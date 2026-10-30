"""Synthetic engineering canary; deliberately faulty setup, never a dispatcher."""
def unique_work(records):
    """Keep the first record for each work unit, preserving input order."""
    result = []
    seen = set()
    for record in records:
        key = record["delivery_id"]
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result
