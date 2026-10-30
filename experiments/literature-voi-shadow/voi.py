#!/usr/bin/env python3
"""Offline shadow value-of-information probe; NO authority or external calls.

EVPI is the *perfect information* ceiling. A candidate search is not recommended
from EVPI alone: an explicit, hypothetical signal likelihood model is required
for expected value of sample information (EVSI). None of the input values are
empirically validated, and no output authorizes real-world execution.
"""
from decimal import Decimal, InvalidOperation
import json
import sys


class InvalidProposal(ValueError):
    pass


LIMIT = 64
EPS = Decimal("0.00000001")


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidProposal(label + ": expected JSON number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise InvalidProposal(label + ": invalid number") from exc
    if not result.is_finite():
        raise InvalidProposal(label + ": non-finite number")
    return result


def collection(value, label):
    if not isinstance(value, list) or not 0 < len(value) <= LIMIT:
        raise InvalidProposal(label + ": required bounded nonempty list")
    return value


def unique_id(value, seen, label):
    if not isinstance(value, str) or not value or value in seen or len(value) > 128:
        raise InvalidProposal(label + ": duplicate or invalid id")
    seen.add(value)


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidProposal("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def result(decision, **extras):
    return {
        "decision": decision,
        "utility_calibration_verified": False,
        "information_model_verified": False,
        "execution_authorized": False,
        "external_calls": 0,
        **extras,
    }


def decide(spec):
    if not isinstance(spec, dict) or type(spec.get("schema_version")) is not int or spec["schema_version"] != 1:
        raise InvalidProposal("SCHEMA_VERSION")
    if spec.get("mode") != "shadow":
        raise InvalidProposal("SHADOW_MODE_REQUIRED")
    actions = collection(spec.get("actions"), "ACTIONS")
    outcomes = collection(spec.get("evidence_outcomes"), "EVIDENCE_OUTCOMES")
    cost = number(spec.get("research_cost"), "research_cost")
    if cost < 0:
        raise InvalidProposal("NEGATIVE_RESEARCH_COST")

    ids, eligible, seen = [], [], set()
    for action in actions:
        if not isinstance(action, dict):
            raise InvalidProposal("INVALID_ACTION")
        aid = action.get("id")
        unique_id(aid, seen, "ACTION")
        gate = action.get("gate")
        if gate not in ("eligible", "hold"):
            raise InvalidProposal("UNVERIFIED_ACTION_GATE")
        ids.append(aid)
        if gate == "eligible":
            eligible.append(aid)
    if not eligible:
        return result("HOLD", reason="NO_ELIGIBLE_ACTION")

    states, seen_states = [], set()
    expected = {aid: Decimal(0) for aid in eligible}
    perfect = Decimal(0)
    total = Decimal(0)
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise InvalidProposal("INVALID_OUTCOME")
        oid = outcome.get("id")
        unique_id(oid, seen_states, "STATE")
        p = number(outcome.get("probability"), "probability")
        if not Decimal(0) < p <= Decimal(1):
            raise InvalidProposal("INVALID_PROBABILITY")
        raw = outcome.get("action_values")
        if not isinstance(raw, dict) or set(raw) != set(ids):
            raise InvalidProposal("MISSING_OR_EXTRA_ACTION_VALUES")
        values = {aid: number(raw[aid], "action_values") for aid in ids}
        states.append((oid, p, values))
        total += p
        perfect += p * max(values[aid] for aid in eligible)
        for aid in eligible:
            expected[aid] += p * values[aid]
    if abs(total - Decimal(1)) > EPS:
        raise InvalidProposal("PROBABILITIES_DO_NOT_SUM_TO_ONE")

    best = sorted(eligible, key=lambda aid: (-expected[aid], aid))[0]
    baseline = expected[best]
    evpi = perfect - baseline
    if evpi < -EPS:
        raise InvalidProposal("EVPI_INCONSISTENT")
    base_fields = {
        "baseline_action": best,
        "evpi_upper_bound": str(max(evpi, Decimal(0))),
        "research_cost_input": str(cost),
    }

    # A perfect-information bound can safely reject an expensive search, but
    # must NOT greenlight a real imperfect search.
    if evpi <= cost + EPS:
        return result("SHADOW_CONTINUE_DIRECT", reason="EVPI_NOT_ABOVE_COST",
                      **base_fields)

    signals = spec.get("research_signals")
    if signals is None:
        return result("SHADOW_NEEDS_SIGNAL_MODEL",
                      reason="EVPI_ONLY_UPPER_BOUND", **base_fields)

    signals = collection(signals, "RESEARCH_SIGNALS")
    seen_signals, likelihoods = set(), []
    likelihood_sums = {state_id: Decimal(0) for state_id, _, _ in states}
    for signal in signals:
        if not isinstance(signal, dict):
            raise InvalidProposal("INVALID_SIGNAL")
        signal_id = signal.get("id")
        unique_id(signal_id, seen_signals, "SIGNAL")
        raw = signal.get("likelihood_by_state")
        if not isinstance(raw, dict) or set(raw) != set(likelihood_sums):
            raise InvalidProposal("SIGNAL_LIKELIHOODS_INCOMPLETE")
        like = {}
        for state_id in likelihood_sums:
            p = number(raw[state_id], "signal_likelihood")
            if not Decimal(0) <= p <= Decimal(1):
                raise InvalidProposal("SIGNAL_LIKELIHOOD_OUT_OF_RANGE")
            like[state_id] = p
            likelihood_sums[state_id] += p
        likelihoods.append(like)
    if any(abs(v - Decimal(1)) > EPS for v in likelihood_sums.values()):
        raise InvalidProposal("SIGNAL_DISTRIBUTION_NOT_NORMALIZED")

    # EVSI = sum_signal max_action sum_state P(state) P(signal|state)
    #             * utility(action,state) - max_action E[utility(action,state)].
    with_sample = Decimal(0)
    for like in likelihoods:
        with_sample += max(
            sum(p * like[oid] * values[aid] for oid, p, values in states)
            for aid in eligible
        )
    evsi = with_sample - baseline
    if evsi < -EPS or evsi > evpi + EPS:
        raise InvalidProposal("EVSI_OUTSIDE_PERFECT_INFORMATION_BOUND")
    evsi = min(max(evsi, Decimal(0)), evpi)
    net = evsi - cost
    return result(
        "SHADOW_SUGGEST_RESEARCH" if net > EPS else "SHADOW_CONTINUE_DIRECT",
        hypothetical_evsi=str(evsi),
        hypothetical_net_information_value=str(net),
        reason="EVSI_ABOVE_COST" if net > EPS else "EVSI_NOT_ABOVE_COST",
        **base_fields,
    )


def main():
    try:
        spec = json.load(sys.stdin, object_pairs_hook=strict_object,
                         parse_constant=lambda _: (_ for _ in ()).throw(
                             InvalidProposal("NONFINITE_JSON_CONSTANT")))
        output = decide(spec)
    except (InvalidProposal, ValueError, TypeError) as exc:
        print(json.dumps(result("HOLD", reason=str(exc)), sort_keys=True))
        return 2
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
