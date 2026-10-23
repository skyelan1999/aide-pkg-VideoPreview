from pathlib import Path
import sys,tarfile,hashlib,json,subprocess
r=Path(__file__).resolve().parents[1];out=Path(sys.argv[1]).resolve();arch=sys.argv[2]
version=(out/'build/version.txt').read_text();license=(out/'build/license.txt').read_text();assert '9.0.2' in version;assert '--enable-gpl' in version and '--enable-nonfree' not in version and '--enable-version3' not in version
assert 'GNU General Public License' in license
for n in ('ffmpeg','ffprobe'):assert (out/'bin'/n).is_file()
dist=r/'dist/engine';dist.mkdir(parents=True,exist_ok=True);archive=dist/f'video-engine-linux-{arch}.tar.gz'
# All licenses, exact configuration and toolchain manifest accompany each binary archive.
with tarfile.open(archive,'w:gz') as t:
 for folder in ('bin','licenses','build'):
  for p in sorted((out/folder).rglob('*')):
   if p.is_file() and not p.name.endswith('-make.log'):t.add(p,arcname=str(p.relative_to(out)),recursive=False)
j={'platform':'linux-'+arch,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'bytes':archive.stat().st_size,'license':'GPL-2.0-or-later','ffmpeg':'9.0.2','sourceLock':json.loads((r/'runtime/source-lock.json').read_text()),'binaryVersion':version,'runtimeLibraries':(out/'build/system-libraries.txt').read_text()}
(archive.with_suffix('.json')).write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
