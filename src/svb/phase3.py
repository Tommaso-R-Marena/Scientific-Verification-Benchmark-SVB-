"""Validate the internally frozen proposal/pilot; this is not scientific validation."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
from .core import Invalid,read
from .adjudication import validate_context,digest_bytes
from .taxonomy import VERSION,validate_assessment
ROOT=Path(__file__).resolve().parents[2]


def archive(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or any(Path(n).is_absolute() or '..' in Path(n).parts or '\\' in n for n in names):
            raise Invalid('unsafe or duplicate archive path')
        if sum(x.file_size for x in z.infolist())>64*1024*1024:raise Invalid('archive too large')
        return {n:z.read(n) for n in names}


def validate(root=ROOT):
    m=read(root/'data/v0.4.0/manifest.json')
    if m['schema_version']!=VERSION or m['human_reviews_completed']!=0 or m['models_executed']!=0:
        raise Invalid('wrong frozen proposal or invented executions')
    for name,h in m['files'].items():
        p=(root/name).resolve()
        if not p.is_relative_to(root.resolve()) or digest_bytes(p.read_bytes())!=h:raise Invalid('Phase III frozen artifact mismatch: '+name)
    pilot=root/'data/v0.4.0/pilot';context=read(pilot/'coordinator_context.json');packets,candidates=validate_context(context)
    if len(packets)!=12 or len(candidates)!=12 or len({p['source_family'] for p in packets.values()})!=5:
        raise Invalid('unexpected pilot size')
    source_bytes=(pilot/'source_materials.zip').read_bytes();sources=archive(source_bytes)
    registry=json.loads(sources['source_registry.json'])
    for src in registry['sources'].values():
        for a in src['artifacts']:
            b=sources[a['package_path']]
            if digest_bytes(b)!=a['sha256'] or len(b)!=a['bytes']:raise Invalid('source archive corruption')
    for stage in ('reference','candidate'):
        files=archive((pilot/f'{stage}_review.zip').read_bytes());pm=json.loads(files.pop('manifest.json'))
        if pm['human_reviews_completed']!=0 or pm['actual_blinding_established'] or pm['protected_holdout']:
            raise Invalid('unsupported review/blinding claim')
        if pm['files']!={n:digest_bytes(b) for n,b in files.items()}:raise Invalid('reviewer package content mismatch')
        if json.loads(files['source_bundle.json'])['sha256']!=digest_bytes(source_bytes):raise Invalid('shared source hash mismatch')
        if json.loads(files['packets.json'])!=[p['packet'] for p in context['packets']]:raise Invalid('review packet/context mismatch')
        f=json.loads(files['blank_response.json'])
        if f['origin'] is not None or f['reviewer_code'] is not None or f['declaration']['human_attestation'] is not None:
            raise Invalid('blank form asserts human provenance')
        if stage=='reference':
            if 'candidates.json' in files or any(j['legacy_labels'] or j['category_relation'] is not None for j in f['judgments']):
                raise Invalid('reference package discloses candidate/reference judgments')
        elif json.loads(files['candidates.json'])!=context['candidates']:raise Invalid('raw candidate/context mismatch')
    for x in read(root/'data/v0.4.0/taxonomy_examples.json'):validate_assessment(x['assessment'])
    return {'schema_version':VERSION,'manifest_sha256':digest_bytes((root/'data/v0.4.0/manifest.json').read_bytes()),
        'reference_packets':len(packets),'candidate_responses':len(candidates),'source_families':5,
        'human_reviews_completed':0,'new_model_inference':0,'scientific_taxonomy_validated':False,'actual_blinding_established':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['validate']);p.parse_args()
    try:print(json.dumps(validate(),sort_keys=True))
    except (Invalid,OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
