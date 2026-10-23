from pathlib import Path
import json,zipfile,hashlib
r=Path(__file__).resolve().parents[1];html=(r/'viewer.template.html').read_text()
for key,f in [('BRIDGE','assets/bridge.js'),('MODEL','assets/model.js'),('PLAYER','assets/player.js')]:html=html.replace('/*'+key+'*/',(r/f).read_text())
(r/'viewer.html').write_text(html)
out=r/'dist';out.mkdir(exist_ok=True);v=json.loads((r/'manifest.json').read_text())['version'];p=out/f'aide-pkg-video-preview-v{v}.zip'
(r/'assets/THIRD_PARTY_NOTICES.md').write_text((r/'THIRD_PARTY_NOTICES.md').read_text())
files=['manifest.json','index.js','viewer.html','native/inspect.py','LICENSE','README.md','THIRD_PARTY_NOTICES.md','licenses/Aide-MIT.txt','native/media.js','native/engine-install.js','native/extract-engine.py','native/media-worker.py','runtime/catalog.json','assets/THIRD_PARTY_NOTICES.md','assets/licenses/FFmpeg-GPLv2.txt','assets/licenses/x264-COPYING.txt']
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in files:
  i=zipfile.ZipInfo(name,(2026,10,23,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,(r/name).read_bytes())
d=hashlib.sha256(p.read_bytes()).hexdigest();(out/'SHA256SUMS').write_text(f'{d}  {p.name}\n');print(json.dumps({'file':str(p),'bytes':p.stat().st_size,'sha256':d}))
