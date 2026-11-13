"""Compare subject working trees to the local-only initial byte fingerprint."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
before=R/'results/local/subject_snapshot_before.json'
if not before.exists():
    raise SystemExit('Initial local-only snapshot unavailable; cannot assert historical nonmodification.')
a=json.loads(before.read_text());out={}
for name,old in a.items():
 p=Path('/workspace')/name
 files=subprocess.check_output(['git','-C',str(p),'ls-files','-z']).split(b'\0')
 hashes={f.decode():hashlib.sha256((p/f.decode()).read_bytes()).hexdigest() for f in files if f and (p/f.decode()).is_file()}
 status=subprocess.check_output(['git','-C',str(p),'status','--porcelain=v1'],text=True)
 commit=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
 out[name]={'commit':commit,'tracked_file_count':len(hashes),'tracked_bytes_unchanged':hashes==old['tracked_files'], 'status_unchanged':status==old['status'],'head_unchanged':commit==old['commit'],'status_before':old['status'],'status_after':status}
(R/'results/subject_integrity.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
assert all(v['tracked_bytes_unchanged'] and v['status_unchanged'] and v['head_unchanged'] for v in out.values())
print('All three subject HEADs, tracked file bytes and Git statuses unchanged.')
