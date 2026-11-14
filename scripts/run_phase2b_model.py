"""Phase IIb offline model runner: categorical, prose and full-schema interfaces.

Consumes raw-only prompt exports, not datasets or reference answers. Optional
category-token constraints are a declared syntax intervention, not proof of
scientific reasoning. Frozen older runners are not imported or modified.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
from typing import Any

PROJECT=Path(__file__).resolve().parents[1]
LABELS=('formally_established','computationally_established','empirically_supported',
        'refuted','insufficient_evidence','disputed_or_unresolved')
SPECS={
 'qwen-0.5b':{'id':'Qwen/Qwen2.5-0.5B-Instruct','revision':'7ae557604adf67be50417f59c2c2f167def9a775','directory':'Qwen2.5-0.5B-Instruct','weights':'fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe'},
 'qwen-1.5b':{'id':'Qwen/Qwen2.5-1.5B-Instruct','revision':'989aa7980e4cf806f80c7fef2b1adb7bc71aa306','directory':'Qwen2.5-1.5B-Instruct','weights':'dd924a11b4c220f385b51ffa522daea7c9f3d850e31b162bb5661df483c6d3ee'},
 'qwen-3b':{'id':'Qwen/Qwen2.5-3B-Instruct','revision':'aa8e72537993ba99e69dfaafa59ed015b17504d1','directory':'Qwen2.5-3B-Instruct','weight_files':{'model-00001-of-00002.safetensors':'67347b23fb4165b652eb6611f5e1f2a06dfcddba8e909df1b2b0b1857bee06c2','model-00002-of-00002.safetensors':'a40d941d0e7e0b966ad8b62bb6d6b7c88cce1299197b599d9d0a4ce59aabfc1d'}}}
class InputError(ValueError): pass

def pairs(ps):
 d={}
 for k,v in ps:
  if k in d:raise InputError('duplicate JSON key')
  d[k]=v
 return d

def loads(s):
 def fp(x):
  v=float(x)
  if not math.isfinite(v):raise InputError('nonfinite JSON')
  return v
 try:return json.loads(s,object_pairs_hook=pairs,parse_float=fp,parse_constant=lambda _:(_ for _ in ()).throw(InputError('nonfinite JSON')))
 except (ValueError,RecursionError) as e:raise InputError(str(e)) from e

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def load_prompts(path):
 p=Path(path)
 if p.stat().st_size>10_000_000:raise InputError('prompt bundle too large')
 rows=[];seen=set()
 for line in p.read_text().splitlines():
  if not line.strip():continue
  r=loads(line)
  if not isinstance(r,dict) or set(r)!={'id','task','condition','messages'}:raise InputError('prompt allowlist is id,task,condition,messages')
  if r['task'] not in ('A','B','C'):raise InputError('task must be A, B or C')
  if any(not isinstance(r[k],str) or not r[k] or len(r[k])>160 for k in ('id','condition')):raise InputError('bounded text IDs required')
  key=(r['id'],r['task'],r['condition'])
  if key in seen:raise InputError('duplicate id/task/condition')
  seen.add(key)
  if not isinstance(r['messages'],list) or not 1<=len(r['messages'])<=4:raise InputError('bounded chat messages required')
  for m in r['messages']:
   if not isinstance(m,dict) or set(m)!={'role','content'} or m['role'] not in ('system','user') or not isinstance(m['content'],str) or not m['content'] or len(m['content'])>100000:raise InputError('invalid message')
  if r['messages'][-1]['role']!='user':raise InputError('last message must be user')
  rows.append(r)
 if not rows:raise InputError('empty bundle')
 return rows

def inside_output(path):
 p=Path(path).resolve()
 if not p.is_relative_to(PROJECT.resolve()):raise InputError('output must remain inside SVB')
 if p.exists():raise InputError('refuse to overwrite experiment artifact')
 return p

class CategoryTrie:
 """Allow exactly six tokenizer category sequences followed by EOS."""
 def __init__(self,sequences,eos):
  if len(sequences)!=len(LABELS) or len({tuple(x) for x in sequences})!=len(LABELS) or any(not s for s in sequences):raise InputError('six distinct nonempty category sequences required')
  if not isinstance(eos,int) or any(eos in s for s in sequences):raise InputError('EOS must be distinct from category tokens')
  self.paths=[tuple(s)+(eos,) for s in sequences];self.eos=eos
 def allowed(self,suffix):
  prefix=tuple(suffix)
  allowed=sorted({p[len(prefix)] for p in self.paths if len(p)>len(prefix) and p[:len(prefix)]==prefix})
  if not allowed:raise InputError('generated prefix left category trie')
  return allowed

def exact_category(raw):
 """Diagnostic formatting check only: whitespace trim, no quotes/fence repair."""
 if not isinstance(raw,str):return None
 text=raw.strip()
 return text if text in LABELS else None

def validate_model(key,model_dir,access_path):
 spec=SPECS[key];access=loads(Path(access_path).read_text());m=access['models'][key]
 if m['id']!=spec['id'] or m['revision']!=spec['revision']:raise InputError('model identity mismatch')
 expected_weights=spec.get('weight_files',{'model.safetensors':spec.get('weights')})
 needed={'LICENSE','README.md','config.json','generation_config.json','merges.txt','tokenizer.json','tokenizer_config.json','vocab.json'}|set(expected_weights)
 if 'weight_files' in spec:needed.add('model.safetensors.index.json')
 if not needed<=set(m['files_sha256']):raise InputError('incomplete model capsule')
 for name,digest in m['files_sha256'].items():
  p=(model_dir/name).resolve()
  if not p.is_relative_to(model_dir.resolve()) or not p.is_file() or sha(p)!=digest:raise InputError('model file hash mismatch: '+name)
 if any(m['files_sha256'][name]!=digest for name,digest in expected_weights.items()):raise InputError('weight identity does not match pinned authoritative digest')
 return m

def run(args):
 rows=load_prompts(args.prompts)
 if args.limit is not None:rows=rows[:args.limit]
 out=inside_output(args.output);meta_path=inside_output(out.with_suffix('.run.json'));out.parent.mkdir(parents=True,exist_ok=True)
 spec=SPECS[args.model];model_dir=args.model_dir or PROJECT/'results/local/models'/spec['directory']
 capsule=validate_model(args.model,model_dir,args.access)
 os.environ.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_IMPLICIT_TOKEN':'1','HF_HUB_DISABLE_TELEMETRY':'1'})
 import torch,transformers
 from transformers import AutoTokenizer,AutoModelForCausalLM
 torch.set_num_threads(args.threads);torch.set_num_interop_threads(1);torch.manual_seed(0);torch.use_deterministic_algorithms(True)
 start=time.time()
 tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.eval()
 sequences=[tokenizer.encode(label,add_special_tokens=False) for label in LABELS]
 if any(tokenizer.decode(seq,skip_special_tokens=False)!=label for seq,label in zip(sequences,LABELS)):raise InputError('category tokenizer roundtrip mismatch')
 trie=CategoryTrie(sequences,tokenizer.eos_token_id)
 caps={'A':args.max_a,'B':args.max_b,'C':args.max_c}
 meta={'format':'svb-phase2b-model-run-v1','model_key':args.model,'model_id':spec['id'],'revision':spec['revision'],'weights_sha256':capsule['files_sha256'].get('model.safetensors',hashlib.sha256(json.dumps(spec.get('weight_files',{}),sort_keys=True,separators=(',',':')).encode()).hexdigest()),'weight_files_sha256':{k:v for k,v in capsule['files_sha256'].items() if k.endswith('.safetensors')},'runner_sha256':sha(Path(__file__)),'prompt_file_sha256':sha(args.prompts),'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,'device':'cpu','dtype':'float32','attention':'eager','threads':args.threads,'seed':0,'do_sample':False,'max_input_tokens':args.max_input_tokens,'new_token_caps':caps,'prompt_truncation':False,'constrained_a':args.constrained_a,'category_constraints':{'labels':list(LABELS),'sequences':sequences,'eos_token_id':tokenizer.eos_token_id,'method':'prefix-allowed category trie plus EOS; syntax intervention only'},'bundle_records':len(load_prompts(args.prompts)),'selected_records':len(rows),'model_load_seconds':time.time()-start,'paid_api_calls':0,'credential_use':False,'reference_labels_loaded':False,'scoring_performed':False,'records':[]}
 meta_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
 with out.open('x') as f:
  for i,p in enumerate(rows):
   begin=time.perf_counter();cap=caps[p['task']]
   r={'id':p['id'],'task':p['task'],'condition':p['condition'],'model_key':args.model,'model_id':spec['id'],'model_revision':spec['revision'],'constrained_a':bool(args.constrained_a and p['task']=='A'),'prompt_sha256':hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'status':'execution_error','raw_text':None,'input_tokens':None,'output_tokens':0,'max_new_tokens':cap,'input_truncated':False,'output_reached_token_limit':False}
   try:
    batch=tokenizer.apply_chat_template(p['messages'],add_generation_prompt=True,return_tensors='pt');n=batch.shape[-1];r['input_tokens']=n
    if n>args.max_input_tokens:raise InputError(f'{n} input tokens exceed cap {args.max_input_tokens}; no truncation')
    kwargs={}
    if r['constrained_a']:
     kwargs['prefix_allowed_tokens_fn']=lambda batch_id,ids:trie.allowed(ids.tolist()[n:])
    with torch.inference_mode():
     gen=model.generate(batch,attention_mask=torch.ones_like(batch),do_sample=False,max_new_tokens=cap,pad_token_id=tokenizer.eos_token_id,temperature=None,top_p=None,top_k=None,use_cache=True,**kwargs)
    tokens=gen[0,n:];r['output_tokens']=len(tokens);r['raw_text']=tokenizer.decode(tokens,skip_special_tokens=True);r['status']='completed';r['output_reached_token_limit']=len(tokens)>=cap
   except Exception as e:r['error']={'type':type(e).__name__,'message':str(e)[:1000]}
   r['seconds']=time.perf_counter()-begin
   f.write(json.dumps(r,sort_keys=True,allow_nan=False)+'\n');f.flush()
   meta['records'].append({k:r[k] for k in ('id','task','condition','status','input_tokens','output_tokens','seconds','output_reached_token_limit')});meta_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
   print(json.dumps({'index':i+1,'selected':len(rows),'id':p['id'],'task':p['task'],'condition':p['condition'],'status':r['status'],'tokens':r['output_tokens'],'seconds':r['seconds']}),flush=True)
 meta['output_sha256']=sha(out);meta['elapsed_seconds']=time.time()-start;meta_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
 return meta

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prompts',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--model',choices=SPECS,required=True);p.add_argument('--model-dir',type=Path);p.add_argument('--access',type=Path,default=PROJECT/'results/v0.3.0/model_access.json');p.add_argument('--threads',type=int,default=4);p.add_argument('--max-input-tokens',type=int,default=4096);p.add_argument('--max-a',type=int,default=24);p.add_argument('--max-b',type=int,default=128);p.add_argument('--max-c',type=int,default=384);p.add_argument('--constrained-a',action='store_true');p.add_argument('--limit',type=int)
 args=p.parse_args()
 if not 1<=args.threads<=8 or not 128<=args.max_input_tokens<=8192 or any(not 1<=x<=512 for x in (args.max_a,args.max_b,args.max_c)) or args.limit is not None and args.limit<1:p.error('resource limits outside supported range')
 try:run(args)
 except (InputError,OSError,KeyError,ImportError) as e:print(json.dumps({'error':type(e).__name__,'message':str(e)}),file=sys.stderr);raise SystemExit(2)
if __name__=='__main__':main()
