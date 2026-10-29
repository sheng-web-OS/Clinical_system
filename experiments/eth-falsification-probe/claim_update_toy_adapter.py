#!/usr/bin/env python3
"""Fictional claim-update demonstration, not a medical / model reasoner."""
import json
import re
import sys

p=json.load(sys.stdin)
text=p['case_text']
if 'verified: signed by the submitter' in text:
    signature='supported'; decision='Transfer because a verified signature is documented'
    support='sufficient'
elif 'verified: the document is not signed' in text:
    signature='refuted'; decision='Hold because an unsigned document is confirmed'
    support='sufficient'
else:
    signature='undetermined'; decision='Request signature-status verification because existing evidence is insufficient'
    support='insufficient'
question=next(k for k,v in p['candidate_questions'].items() if 'signature status?' in v)
choice=next(k for k,v in p['candidate_decisions'].items() if v==decision)
fact=re.search(r'signature record reads \[([^]]+)\]',text).group(1)
claim_statuses={}
for k,v in p['candidate_claims'].items():
    if 'verified to have signed' in v: state=signature
    elif 'cover is blue' in v: state='refuted' if 'green' in text else 'supported'
    elif 'has a cover' in v: state='supported'
    else: raise ValueError('unknown claim')
    claim_statuses[k]=state
out={'probe_id':p['probe_id'],'packet_sha256':p['packet_sha256'],
    'question_id':question,'evidence_ids':[fact], 'decision_id':choice,
    'review_flags':[], 'support_status':support,'claim_statuses':claim_statuses}
print(json.dumps(out))
