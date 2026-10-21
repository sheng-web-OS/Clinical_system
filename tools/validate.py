import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'knowledge/catalog.json').read_text())
evidence=json.loads((ROOT/'knowledge/evidence.json').read_text())
ids=set(); source_ids={s['id'] for s in evidence['sources']}
for unit in catalog['units']:
    assert unit['id'] not in ids, f"duplicate id: {unit['id']}"
    ids.add(unit['id'])
    path=ROOT/unit['file']
    assert path.is_file() and path.suffix=='.md', f"missing unit: {path}"
    assert unit['status'] in ('draft','blocked','published')
    assert unit['kind'] in ('system','clinical')
    assert set(unit.get('sources',[])) <= source_ids, f"unknown sources: {unit['id']}"
    if unit['kind']=='clinical' and unit['status']=='published':
        assert unit['sources'], f"clinical unit lacks sources: {unit['id']}"
        assert (ROOT/'reviews'/f"{unit['id']}.json").is_file(), f"clinical unit lacks audit: {unit['id']}"
print(f"VALID: {len(ids)} units, {len(source_ids)} registered sources")
