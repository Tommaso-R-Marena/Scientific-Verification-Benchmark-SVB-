"""Offline, data-only inference runner for pinned Qwen 0.5B public weights.

Prompts are independently exported JSONL, never benchmark/oracle objects. This
runner does not assign reference labels, repair output, or execute model code.
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

PROJECT = Path(__file__).resolve().parents[1]
MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
REVISION = '7ae557604adf67be50417f59c2c2f167def9a775'
MAX_FILE_BYTES = 10_000_000

class InputError(ValueError):
    """Invalid data-only prompt bundle; inference must not begin."""

def pairs(ps):
    result = {}
    for k,v in ps:
        if k in result: raise InputError('duplicate JSON key')
        result[k] = v
    return result

def strict_loads(text:str) -> Any:
    def floating(s):
        value=float(s)
        if not math.isfinite(value): raise InputError('nonfinite number')
        return value
    try:
        return json.loads(text,object_pairs_hook=pairs,parse_float=floating,
                          parse_constant=lambda _: (_ for _ in ()).throw(InputError('nonfinite number')))
    except (ValueError,RecursionError) as e:
        raise InputError(str(e)) from e

def load_prompts(path:Path) -> list[dict[str,Any]]:
    if path.stat().st_size > MAX_FILE_BYTES: raise InputError('prompt bundle too large')
    prompts=[];seen=set()
    for line_number,text in enumerate(path.read_text().splitlines(),1):
        if not text.strip(): continue
        row=strict_loads(text)
        if not isinstance(row,dict) or set(row)!={'id','condition','messages'}:
            raise InputError(f'line {line_number}: prompt fields must be id, condition, messages only')
        if any(not isinstance(row[k],str) or not row[k] or len(row[k])>120 for k in ('id','condition')):
            raise InputError('bounded id and condition strings required')
        key=row['id'],row['condition']
        if key in seen: raise InputError('duplicate prompt id/condition')
        seen.add(key)
        if not isinstance(row['messages'],list) or not 1<=len(row['messages'])<=4:
            raise InputError('one to four chat messages required')
        for m in row['messages']:
            if not isinstance(m,dict) or set(m)!={'role','content'}:
                raise InputError('message fields must be role and content only')
            if m['role'] not in ('system','user') or not isinstance(m['content'],str) or not m['content'] or len(m['content'])>100000:
                raise InputError('invalid role/content')
        if row['messages'][-1]['role']!='user': raise InputError('last message must be user')
        prompts.append(row)
    if not prompts: raise InputError('no prompts supplied')
    return prompts

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def inside_output(path:Path)->Path:
    out=path.resolve()
    if not out.is_relative_to(PROJECT.resolve()): raise InputError('output must stay inside SVB project')
    if out.exists(): raise InputError('refusing to overwrite prior inference record')
    return out

def validate_model(model_dir:Path,access_file:Path)->dict:
    access=strict_loads(access_file.read_text())
    if access['model']['id']!=MODEL_ID or access['model']['revision']!=REVISION:
        raise InputError('unexpected model identity/revision')
    for name, expected in access['model']['files_sha256'].items():
        p=(model_dir/name).resolve()
        if not p.is_relative_to(model_dir.resolve()) or not p.is_file() or sha(p)!=expected:
            raise InputError('model file hash mismatch: '+name)
    if not (model_dir/'model.safetensors').is_file(): raise InputError('safetensors required')
    return access

def run(args)->dict:
    # No implicit credentials, downloads or remote Python code during inference.
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    os.environ['HF_HUB_DISABLE_TELEMETRY']='1';os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN']='1'
    prompts=load_prompts(args.prompts)
    if args.limit is not None: prompts=prompts[:args.limit]
    out=inside_output(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    metadata_path=inside_output(out.with_suffix('.run.json'))
    access=validate_model(args.model_dir,args.access)
    import torch
    import transformers
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(args.threads);torch.set_num_interop_threads(1)
    torch.manual_seed(0);torch.use_deterministic_algorithms(True)
    started=time.time()
    tokenizer=AutoTokenizer.from_pretrained(args.model_dir,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(args.model_dir,local_files_only=True,
           trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,
           attn_implementation="eager")
    model.eval()
    meta={'model_id':MODEL_ID,'revision':REVISION,'weights_sha256':access['model']['files_sha256']['model.safetensors'],
          'runner_sha256':sha(Path(__file__)),'prompt_file_sha256':sha(args.prompts),
          'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,
          'device':'cpu','dtype':'float32','attention_implementation':'eager','threads':args.threads,'seed':0,'do_sample':False,
          'max_new_tokens':args.max_new_tokens,'max_input_tokens':args.max_input_tokens,
          'prompt_truncation':False,'model_load_seconds':time.time()-started,
          'paid_api_calls':0,'credential_use':False,'scoring_performed':False,
          'attention_warning_analysis':'Transformers warns because config.sliding_window=32768 is nonnull; official config.use_sliding_window=false. Recorded input/output caps remain below that window. No config or weights altered.',
          'bundle_records':len(load_prompts(args.prompts)),'selected_records':len(prompts),'records':[]}
    # Metadata is written before outputs, then updated per record to retain crashes.
    metadata_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
    with out.open('x') as f:
        for index,p in enumerate(prompts):
            begin=time.perf_counter()
            row={'id':p['id'],'condition':p['condition'],'model_id':MODEL_ID,'model_revision':REVISION,
                 'prompt_sha256':hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                 'status':'execution_error','raw_text':None,'input_tokens':None,'output_tokens':0,
                 'truncated_input':False,'output_reached_token_limit':False}
            try:
                batch=tokenizer.apply_chat_template(p['messages'],add_generation_prompt=True,return_tensors='pt')
                n=batch.shape[-1];row['input_tokens']=n
                if n>args.max_input_tokens: raise InputError(f'input has {n} tokens, cap {args.max_input_tokens}; no truncation performed')
                with torch.inference_mode():
                    generated=model.generate(batch,attention_mask=torch.ones_like(batch),do_sample=False,
                         max_new_tokens=args.max_new_tokens,pad_token_id=tokenizer.eos_token_id,
                         temperature=None,top_p=None,top_k=None,
                         use_cache=True)
                tokens=generated[0,n:];row['output_tokens']=len(tokens)
                row['raw_text']=tokenizer.decode(tokens,skip_special_tokens=True)
                row['status']='completed'
                row['output_reached_token_limit']=len(tokens)>=args.max_new_tokens
                # No JSON extraction, repair or retries based on answer validity.
            except Exception as e:
                row['error']={'type':type(e).__name__,'message':str(e)[:1000]}
            row['seconds']=time.perf_counter()-begin
            f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n');f.flush()
            meta['records'].append({k:row[k] for k in ('id','condition','status','input_tokens','output_tokens','seconds','output_reached_token_limit')})
            metadata_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
            print(json.dumps({'index':index+1,'selected':len(prompts),'id':p['id'],'condition':p['condition'],'status':row['status'],'seconds':row['seconds'],'tokens':row['output_tokens']}),flush=True)
    meta['output_sha256']=sha(out);meta['elapsed_seconds']=time.time()-started
    metadata_path.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n')
    return meta

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prompts',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--model-dir',type=Path,default=PROJECT/'results/local/models/Qwen2.5-0.5B-Instruct')
    p.add_argument('--access',type=Path,default=PROJECT/'results/v0.2.0/model_access.json')
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--max-new-tokens',type=int,default=256)
    p.add_argument('--max-input-tokens',type=int,default=4096)
    p.add_argument('--limit',type=int)
    args=p.parse_args()
    if not 1<=args.threads<=8 or not 1<=args.max_new_tokens<=1024 or not 128<=args.max_input_tokens<=16384 or args.limit is not None and args.limit<1:
        p.error('resource limit outside supported range')
    try: run(args)
    except (InputError,OSError,KeyError,ImportError) as e:
        print(json.dumps({'error':type(e).__name__,'message':str(e)}),file=sys.stderr);raise SystemExit(2)

if __name__=='__main__':main()
