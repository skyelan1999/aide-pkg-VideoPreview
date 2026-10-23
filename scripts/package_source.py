"""Create the exact engine corresponding-source release asset, never a download-only offer."""
from pathlib import Path
import tarfile,hashlib,json,io
r=Path(__file__).resolve().parents[1];dist=r/'dist';dest=dist/'video-engine-corresponding-source-v0.1.0.tar.gz'
lock=json.loads((r/'runtime/source-lock.json').read_text())
for k in ('ffmpeg','x264'):
 p=r/'runtime/sources'/lock[k]['archive'];assert hashlib.sha256(p.read_bytes()).hexdigest()==lock[k]['sha256']
files={}
for n in ['runtime/build.sh','runtime/Dockerfile','runtime/source-lock.json','THIRD_PARTY_NOTICES.md']:
 files[n]=(r/n).read_bytes()
for p in (r/'runtime/sources').iterdir():files['runtime/sources/'+p.name]=p.read_bytes()
for arch in ('arm64','amd64'):
 with tarfile.open(dist/f'ci-{arch}/video-engine-linux-{arch}.tar.gz') as t:
  for m in t.getmembers():
   if m.isfile() and m.name.startswith(('build/','licenses/')):files['actual-builds/'+arch+'/'+m.name]=t.extractfile(m).read()
 files['actual-builds/'+arch+'/artifact.json']=(dist/f'ci-{arch}/video-engine-linux-{arch}.tar.json').read_bytes()
files['BUILDING.md']=b'''# Complete corresponding source for Video Preview optional engines 0.1.0\n\nExact upstream sources are in runtime/sources, unchanged. SHA-256 and official provenance are in runtime/source-lock.json. No patches are applied.\n\nOn Linux ARM64 or AMD64, install Docker then run:\n\n    docker build -f runtime/Dockerfile -t video-engine-builder .\n    mkdir -p engine-out\n    docker run --rm --network none -v "$PWD/engine-out:/out" video-engine-builder\n\nThe Dockerfile pins the base toolchain multiarch digest. Actual configure files, copyright texts, compiler/system package versions and runtime library records for each distributed binary are in actual-builds/. Engine linking uses x264 statically and system libc/libm only. No nonfree/version3 option. This is a configuration-only integration, with no upstream source modifications.\n\nGPL-2.0-or-later for the optional combined engine. Preserve all copyright notices and provide these corresponding sources with redistribution. This source archive is served alongside the exact binary files on the same GitHub Release without charge. The application wrapper remains separately licensed MIT.\n'''
with tarfile.open(dest,'w:gz') as t:
 for n,b in sorted(files.items()):
  m=tarfile.TarInfo(n);m.size=len(b);m.mtime=1792713600;m.mode=0o755 if n.endswith('.sh') else 0o644;t.addfile(m,io.BytesIO(b))
with tarfile.open(dest) as t:
 names=t.getnames();assert all('runtime/sources/'+lock[k]['archive'] in names for k in ('ffmpeg','x264'));assert all('actual-builds/'+a+'/build/config.h' in names for a in ('arm64','amd64'))
result={'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()};print(json.dumps(result))
(dist/'source-artifact.json').write_text(json.dumps(result,indent=2)+'\n')
