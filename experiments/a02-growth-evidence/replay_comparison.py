#!/usr/bin/env python3
"""Reproduce isolated synthetic #225 vs A02-01 comparison (no network).

Usage: python replay_comparison.py --old-evaluator /other/checkout/tools/compare_skill_transfer.py
Do NOT use this as a blinded benchmark, clinical review, or an autonomy score.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from test_growth_leakage import sample
from audit_growth_leakage import audit

EXPECTED_OLD_BLOB = '65645acf9d8df981c1ea6d359588c7075cb479aa'
ARMS = ('native','retrieval','skill')


def old_module(path):
    data=Path(path).read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if digest!=EXPECTED_OLD_BLOB:
        raise ValueError('OLD_EVALUATOR_BLOB_MISMATCH: '+digest)
    spec=importlib.util.spec_from_file_location('frozen_225_evaluator',path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixture():
    cases=[('t','transfer'),('n','normal'),('b','boundary')]
    suite={'schema_version':1,'id':'a02-replay-synthetic','exposure':'development',
           'retrieval_pack_sha256':'d'*64,'candidate_skill_sha256':'e'*64,
           'cases':[{'id':cid,'role':role,'source_sha256':('a','b','c')[i]*64}
                    for i,(cid,role) in enumerate(cases)]}
    records=[]
    for i,(cid,role) in enumerate(cases):
        for arm in ARMS:
            correct=role!='transfer' or arm=='skill'
            records.append({'case_id':cid,'arm':arm,'attempt_status':'COMPLETED',
                'source_sha256':('a','b','c')[i]*64,'decision_correct':correct,
                'first_pass':correct,'unsafe':False,'hinted':False,'false_alarm':False,
                'article_retrieval_visible':arm!='native',
                'candidate_skill_visible':arm=='skill',
                'retrieval_pack_sha256':None if arm=='native' else 'd'*64,
                'loaded_skill_sha256':'e'*64 if arm=='skill' else None,
                'skill_applied':arm=='skill' and role=='transfer',
                'worker_context':f'worker-{cid}-{arm}',
                'reviewer_context':'synthetic-review',
                'trace_ref':f'trace-{cid}-{arm}',
                'model':'fixed','effort':'fixed','tools_scope':'fixed',
                'token_budget':'fixed','owner_minutes':None})
    run={'schema_version':1,'suite_id':suite['id'],
         'suite_sha256':'','candidate_commit':'f'*40,'records':records}
    cohort=sample()
    for i,c in enumerate(cohort['cases']): c['id']=cases[i][0]
    return suite,run,cohort


def mutations():
    def overlap(s,r,a): a['cases'][2]['family_id']=a['cases'][0]['family_id']
    def dev_overlap(s,r,a): a['cases'][2]['family_id']=a['cases'][1]['family_id']
    def future(s,r,a):
        a['cases'][1]['evidence_available_at']='2026-09-12T00:00:00+00:00'
        a['cases'][1]['evidence_observed_at']='2026-09-13T00:00:00+00:00'
    def late(s,r,a): a['cases'][1]['evidence_observed_at']='2026-09-13T00:00:00+00:00'
    def immature(s,r,a): a['cases'][0]['label_mature_at']='2026-10-02T01:00:00+00:00'
    def timezone(s,r,a): a['cases'][2]['decision_at']='2026-09-17T00:00:00'
    def shared_source(s,r,a):
        for c in s['cases']: c['source_sha256']='a'*64
        for x in r['records']: x['source_sha256']='a'*64
    def purported_family(s,r,a):
        # The reporter has hidden the true case-family collision; no source
        # checker can recover it from these unverified declarative labels.
        a['cases'][2]['family_id']='different-label-same-case'
    def hinted(s,r,a): r['records'][0]['hinted']=True
    def contaminated(s,r,a): r['records'][0]['article_retrieval_visible']=True
    return [
        ('clean','control',lambda s,r,a:None),
        ('same_public_source_different_cases','control',shared_source),
        ('train_holdout_overlap','new_A02',overlap),
        ('dev_holdout_overlap','new_A02',dev_overlap),
        ('future_publication','new_A02',future),
        ('late_observation','new_A02',late),
        ('immature_train_label','new_A02',immature),
        ('naive_timestamp','new_A02',timezone),
        ('forged_family_alias','A02_blind_spot',purported_family),
        ('retrospective_holdout_without_attested_seal','A02_blind_spot',lambda s,r,a:None),
        ('hinted_worker','existing_225',hinted),
        ('native_arm_retrieval','existing_225',contaminated),
    ]


def compare(old):
    rows=[]
    for name,category,change in mutations():
        suite,run,cohort=copy.deepcopy(fixture())
        change(suite,run,cohort)
        run['suite_sha256']=hashlib.sha256(
            json.dumps(suite,sort_keys=True).encode()).hexdigest()
        try:
            verdict=old.evaluate(suite,run,run['suite_sha256'],'d'*64,'e'*64)['verdict']
            original={'accepted':True,'verdict':verdict}
        except (ValueError,KeyError,TypeError) as e:
            original={'accepted':False,'error':str(e)}
        try:
            out=audit(cohort)
            new={'accepted':out['status']!='REJECT','status':out['status'],
                 'codes':[x['code'] for x in out['violations']]}
        except (ValueError,KeyError,TypeError) as e:
            new={'accepted':False,'status':'INVALID_INPUT','error':str(e)}
        rows.append({'scenario':name,'category':category,'original_225':original,'A02':new})
    categories={cat:[r for r in rows if r['category']==cat]
                for cat in ('control','new_A02','existing_225','A02_blind_spot')}
    counts={'total':len(rows),'A02_new_detected':sum(r['original_225']['accepted'] and not r['A02']['accepted'] for r in categories['new_A02']),
            'A02_new_denominator':len(categories['new_A02']),
            'controls_preserved':sum(r['original_225']['accepted'] and r['A02']['accepted'] for r in categories['control']),
            'control_denominator':len(categories['control']),
            'old_existing_detected':sum(not r['original_225']['accepted'] for r in categories['existing_225']),
            'old_existing_denominator':len(categories['existing_225']),
            'A02_blind_spot_cases':sum(r['A02']['accepted'] for r in categories['A02_blind_spot']),
            'blind_spot_denominator':len(categories['A02_blind_spot'])}
    return {'status':'SYNTHETIC_NONBLIND_REPLAY_ONLY',
            'original_225_git_blob_sha1':EXPECTED_OLD_BLOB,'tallies':counts,
            'cases':rows,'genuine_case_family_authenticated':False,
            'growth_score_change_authorized':False,
            'limitations':'Locally authored scenarios; neither true real-world sensitivity nor independent clinical or model evidence.'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--old-evaluator',required=True,type=Path)
    args=p.parse_args()
    print(json.dumps(compare(old_module(args.old_evaluator)),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
