#!/usr/bin/env python3
"""Pure, offline shadow probe: should additional research change a task decision?

Conceptually adapts rational metareasoning / expected value of information.
No scheduling, GitHub writes, model calls, networking, or authority grants.
All utility and probability values are hypothetical inputs, not calibrated facts.
"""
from decimal import Decimal, InvalidOperation
import json
import sys


class InvalidProposal(ValueError):
    pass


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


def decide(spec):
    if not isinstance(spec, dict) or spec.get("schema_version") != 1:
        raise InvalidProposal("SCHEMA_VERSION")
    if spec.get("mode") != "shadow":
        raise InvalidProposal("SHADOW_MODE_REQUIRED")
    actions = spec.get("actions")
    outcomes = spec.get("evidence_outcomes")
    if not isinstance(actions, list) or not actions:
        raise InvalidProposal("ACTIONS_REQUIRED")
    if not isinstance(outcomes, list) or not outcomes:
        raise InvalidProposal("EVIDENCE_OUTCOMES_REQUIRED")
    cost = number(spec.get("research_cost"), "research_cost")
    if cost < 0:
        raise InvalidProposal("NEGATIVE_RESEARCH_COST")

    ids = []
    eligible = []
    for action in actions:
        if not isinstance(action, dict):
            raise InvalidProposal("INVALID_ACTION")
        aid = action.get("id")
        gate = action.get("gate")
        if not isinstance(aid, str) or not aid or aid in ids:
            raise InvalidProposal("DUPLICATE_OR_INVALID_ACTION")
        if gate not in ("eligible", "hold"):
            raise InvalidProposal("UNVERIFIED_ACTION_GATE")
        ids.append(aid)
        if gate == "eligible":
            eligible.append(aid)
    if not eligible:
        return {"decision": "HOLD", "reason": "NO_ELIGIBLE_ACTION",
                "execution_authorized": False}

    seen = set()
    weighted = {aid: Decimal(0) for aid in eligible}
    expected_after = Decimal(0)
    probability_sum = Decimal(0)
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            raise InvalidProposal("INVALID_OUTCOME")
        oid = outcome.get("id")
        if not isinstance(oid, str) or not oid or oid in seen:
            raise InvalidProposal("DUPLICATE_OR_INVALID_OUTCOME")
        seen.add(oid)
        p = number(outcome.get("probability"), "probability")
        if not Decimal(0) < p <= Decimal(1):
            raise InvalidProposal("INVALID_PROBABILITY")
        values = outcome.get("action_values")
        if not isinstance(values, dict) or set(values) != set(ids):
            raise InvalidProposal("MISSING_OR_EXTRA_ACTION_VALUES")
        v = {aid: number(values[aid], "action_values") for aid in ids}
        probability_sum += p
        for aid in eligible:
            weighted[aid] += p * v[aid]
        expected_after += p * max(v[aid] for aid in eligible)
    if abs(probability_sum - Decimal(1)) > Decimal("0.00000001"):
        raise InvalidProposal("PROBABILITIES_DO_NOT_SUM_TO_ONE")
    best = sorted(eligible, key=lambda aid: (-weighted[aid], aid))[0]
    without_research = weighted[best]
    gross = expected_after - without_research
    net = gross - cost
    return {
        "decision": "SHADOW_SUGGEST_RESEARCH" if net > 0 else "SHADOW_CONTINUE_DIRECT",
        "baseline_action": best,
        "hypothetical_gross_information_value": str(gross),
        "hypothetical_net_information_value": str(net),
        "research_cost_input": str(cost),
        "utility_calibration_verified": False,
        "execution_authorized": False,
        "external_calls": 0,
    }


def main():
    try:
        result = decide(json.load(sys.stdin))
    except (InvalidProposal, ValueError, TypeError) as exc:
        print(json.dumps({"decision": "HOLD", "reason": str(exc),
                          "execution_authorized": False}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
