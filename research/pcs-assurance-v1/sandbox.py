"""Read-only subject, denied network/host workspace, fresh writable output only."""
import os,resource,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[2]
SUBJECT=R/'results/local/pcs-assurance/subject'
LEAN=Path('/workspace/.setup/lean').resolve()
def limits():
 resource.setrlimit(resource.RLIMIT_CPU,(240,240))
 resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
 resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024**2,32*1024**2))
 resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def command(work,argv):
 return ['bwrap','--unshare-all','--die-with-parent','--new-session','--clearenv',
 '--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp',
 '--ro-bind',str(SUBJECT),'/subject','--ro-bind',str(LEAN),'/lean','--ro-bind',str(Path(__file__).parent/'worker.py'),'/worker.py',
 '--bind',str(Path(work).resolve()),'/work','--chdir','/work',
 '--setenv','PATH','/lean/bin:/usr/local/bin:/usr/bin','--setenv','HOME','/tmp','--setenv','LANG','C.UTF-8',
 '--setenv','PYTHONDONTWRITEBYTECODE','1','--setenv','PYTHONPATH','/subject','--setenv','PCS_CLAIMCHECK_LEAN','/lean/bin/lean',
 '--setenv','LEAN_NUM_THREADS','1',*argv]
def execute(work,argv,timeout=240):
 cmd=command(work,argv);start=time.monotonic()
 try:
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,preexec_fn=limits,env={'PATH':'/usr/bin:/bin'})
  return {'returncode':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace'),'seconds':time.monotonic()-start,'timed_out':False,'command':cmd}
 except subprocess.TimeoutExpired as e:
  return {'returncode':None,'stdout':(e.stdout or b'').decode(errors='replace'),'stderr':(e.stderr or b'').decode(errors='replace'),'seconds':time.monotonic()-start,'timed_out':True,'command':cmd}
