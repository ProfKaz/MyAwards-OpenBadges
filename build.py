#!/usr/bin/env python3
"""Publish self-issued Open Badges 2.0 personal records (not Microsoft-issued OB2)."""
import json,re,struct,zlib,shutil,sys,html
from pathlib import Path
root=Path(__file__).resolve().parent
cfg=json.loads((root/'config.json').read_text(encoding='utf8'))
base=cfg['base_url'].rstrip('/')
issuer=cfg['issuer']
if not base.startswith('https://'): sys.exit('HTTPS base_url required')
if not issuer['email'] or issuer['email'].startswith('REPLACE_'): sys.exit('Configure a real public issuer contact email')
docs=root/'docs';docs.mkdir(exist_ok=True)
(docs/'.nojekyll').touch()
def put(rel,obj):
 p=docs/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def chunk(t,d):
 return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
def bake(raw, assertion):
 if raw[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('PNG expected')
 meta=b'openbadges\x00\x00\x00\x00\x00'+json.dumps(assertion,ensure_ascii=False,separators=(',',':')).encode('utf8')
 out=bytearray(raw[:8]);pos=8;inserted=False
 while pos<len(raw):
  if pos+12>len(raw):raise ValueError('Truncated PNG')
  size=struct.unpack('>I',raw[pos:pos+4])[0]
  typ=raw[pos+4:pos+8];data=raw[pos+8:pos+8+size]
  original=raw[pos:pos+12+size];pos+=12+size
  if typ in (b'iTXt',b'tEXt') and data.split(b'\x00',1)[0]==b'openbadges':continue
  if typ==b'IDAT' and not inserted:out+=chunk(b'iTXt',meta);inserted=True
  out+=original
  if typ==b'IEND':break
 if not inserted:raise ValueError('IDAT chunk missing')
 return bytes(out)
issuer_id=base+'/issuer/profile.json'
put('issuer/profile.json',{'@context':'https://w3id.org/openbadges/v2','type':'Profile','id':issuer_id,'name':issuer['name'],'url':issuer['url'],'email':issuer['email']})
links=[]
for r in cfg['records']:
 slug=r['slug']
 if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',slug):raise ValueError('Invalid slug '+slug)
 src=root/r['original_image']
 if not src.exists():
  src=docs/'assets'/(slug+'.png')
 if not src.exists():raise FileNotFoundError('Original PNG not found: '+str(src))
 image_rel='assets/'+slug+'.png';dest=docs/image_rel
 dest.parent.mkdir(parents=True,exist_ok=True)
 if src.resolve()!=dest.resolve(): shutil.copyfile(src,dest)
 badge_id=base+'/badges/'+slug+'.json'
 assertion_id=base+'/assertions/'+slug+'.json'
 verify=r['verification_url'];title=r['title']
 badge={'@context':'https://w3id.org/openbadges/v2','type':'BadgeClass','id':badge_id,'name':'Personal record: '+title,'description':'Self-issued reference to independently verifiable achievement; not a Microsoft-issued Open Badge.','image':base+'/'+image_rel,'criteria':{'narrative':'Original credential verification: '+verify},'issuer':issuer_id}
 assertion={'@context':'https://w3id.org/openbadges/v2','type':'Assertion','id':assertion_id,'recipient':cfg['recipient'],'badge':badge_id,'verification':{'type':'hosted'},'issuedOn':r['self_attestation_date'],'evidence':[{'id':verify,'name':'Original credential verification'}]}
 put('badges/'+slug+'.json',badge);put('assertions/'+slug+'.json',assertion)
 (docs/('assets/'+slug+'-openbadges2.png')).write_bytes(bake(src.read_bytes(),assertion))
 links.append('<li>'+html.escape(title)+' — <a href="assets/'+slug+'-openbadges2.png">Open Badges 2.0 image</a> — <a href="'+html.escape(verify,quote=True)+'">verify original certification</a></li>')
(docs/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>MyAwards OpenBadges</title><h1>MyAwards — personal credential references</h1><p>These are self-issued records, not Microsoft-issued Open Badges. Always verify the original credential directly.</p><ul>'+''.join(links)+'</ul></html>',encoding='utf8')
print('Built',len(links),'record(s) to',docs)
