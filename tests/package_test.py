import unittest,zipfile,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class Packaging(unittest.TestCase):
 def test_allowlist_and_notices(self):
  p=next((R/'dist').glob('*.zip'))
  with zipfile.ZipFile(p) as z:
   self.assertIsNone(z.testzip());names=z.namelist();self.assertEqual(len(names),8)
   self.assertIn('licenses/Aide-MIT.txt',names);self.assertIn('THIRD_PARTY_NOTICES.md',names)
   self.assertFalse(any('runtime/' in n or 'ffmpeg' in n or '__pycache__' in n for n in names))
   self.assertIn('Copyright (c) 2026 Skye Lan',z.read('licenses/Aide-MIT.txt').decode())
   self.assertIn('NOT shipped',z.read('THIRD_PARTY_NOTICES.md').decode())
 def test_bridge_provenance(self):
  a=json.loads((R/'docs/license-audit.json').read_text());self.assertEqual(hashlib.sha256((R/'assets/bridge.js').read_bytes()).hexdigest(),a['packageThirdParty'][0]['sha256'])
if __name__=='__main__':unittest.main()
