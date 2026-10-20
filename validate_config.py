#!/usr/bin/env python3
"""Check configuration before publishing. No network requests."""
import json,re,sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
root=Path(__file__).resolve().parent
cfg=json.loads((root/'config.json').read_text(encoding='utf-8'))
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
def url(v):
 try:
  p=urlparse(v);return p.scheme=='https' and bool(p.netloc)
 except (TypeError,ValueError):return False
check(url(cfg.get('base_url','')),'base_url must be HTTPS')
issuer=cfg.get('issuer',{})
for k in ('name','url','email'):check(bool(issuer.get(k)),f'issuer.{k} is required')
check(url(issuer.get('url','')),'issuer.url must be HTTPS')
recipient=cfg.get('recipient',{})
check(recipient.get('type')=='email','recipient.type must be email for this configuration')
check(bool(re.fullmatch(r'[^@\\s]+@[^@\\s]+\\.[^@\\s]+',recipient.get('identity',''))),'recipient.identity must be a valid email')
check(recipient.get('hashed') is False,'hashed recipient must be false unless hashing is implemented')
slugs=set()
for n,r in enumerate(cfg.get('records',[])):
 label=f'records[{n}]';slug=r.get('slug','')
 check(bool(re.fullmatch(r'[a-z0-9][a-z0-9-]*',slug)),label+' invalid slug')
 check(slug not in slugs,label+' duplicate slug');slugs.add(slug)
 check(bool(r.get('title')),label+' title required')
 check(url(r.get('verification_url','')),label+' verification URL must be HTTPS')
 check((root/r.get('original_image','MISSING')).is_file(),label+' source PNG not found')
 for key in ('self_attestation_date','expires'):
  if key=='expires' and not r.get(key):continue
  try:datetime.fromisoformat(r[key].replace('Z','+00:00'))
  except (ValueError,KeyError,AttributeError):errors.append(label+' invalid '+key)
 if r.get('skills') and (not isinstance(r['skills'],list) or not all(isinstance(x,str) and x.strip() for x in r['skills'])):errors.append(label+' invalid skills list')
 if r.get('skills_source'):check(url(r['skills_source']),label+' invalid skills_source')
check(bool(cfg.get('records')),'At least one badge required')
for e in errors:print('ERROR:',e)
print('Validation', 'FAILED' if errors else 'PASSED')
if errors:sys.exit(1)
