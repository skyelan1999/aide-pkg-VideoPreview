import unittest,tarfile,tempfile,io,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class EngineArchive(unittest.TestCase):
 def run_archive(self,name,kind=tarfile.REGTYPE):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.tar.gz';dest=Path(d)/'engine';dest.mkdir()
   with tarfile.open(p,'w:gz') as t:
    x=tarfile.TarInfo(name);x.type=kind;x.size=1 if kind==tarfile.REGTYPE else 0;t.addfile(x,io.BytesIO(b'x') if x.size else None)
   return subprocess.run([sys.executable,str(R/'native/extract-engine.py'),str(p),str(dest)],capture_output=True).returncode
 def test_safe_binary(self):self.assertEqual(self.run_archive('bin/ffmpeg'),0)
 def test_traversal(self):self.assertNotEqual(self.run_archive('../escape'),0)
 def test_absolute(self):self.assertNotEqual(self.run_archive('/bin/ffmpeg'),0)
 def test_symlink(self):self.assertNotEqual(self.run_archive('bin/ffmpeg',tarfile.SYMTYPE),0)
 def test_unexpected_path(self):self.assertNotEqual(self.run_archive('etc/passwd'),0)
if __name__=='__main__':unittest.main()
