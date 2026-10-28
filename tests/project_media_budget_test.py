import importlib.util,json,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('project_media_adapter',Path(__file__).resolve().parents[1]/'native/inspect.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
class CountedPath(str):
 comparisons=0
 def __eq__(self,other):
  type(self).comparisons+=1
  return super().__eq__(other)
 __hash__=str.__hash__
class MediaBudget(unittest.TestCase):
 def test_unique_paths_do_not_scan_every_previous_path(self):
  paths=[CountedPath('owned-prefix/'+'x'*1000+str(i)+'.mp4') for i in range(1000)]
  obj={'tracks':[],'materials':{'videos':[{'id':str(i),'path':p,'material_name':'first-'+str(i)} for i,p in enumerate(paths)]}}
  obj['materials']['videos'].append({'id':'duplicate','path':CountedPath(paths[0]),'material_name':'later-label'})
  payload=json.dumps(obj).encode();self.assertLess(len(payload),adapter.MAX);CountedPath.comparisons=0
  # Count equality operations on the actual decoded strings, without changing
  # their equality/hash semantics or the project adapter's media traversal.
  with patch.object(adapter.json,'loads',return_value=obj):out=adapter.inspect(payload,'owned.json')
  operations=CountedPath.comparisons
  self.assertLess(operations,3000)
  self.assertEqual([str(m['path']) for m in out['media']],[str(p) for p in paths]);self.assertEqual(out['media'][0]['name'],'first-0');self.assertEqual(out['media'][0]['status'],'unverified')
  print('media equality operations:',operations)
 def test_limit_and_per_inspection_isolation(self):
  obj={'tracks':[],'materials':{'videos':[{'id':str(i),'path':str(i)+'.mp4'} for i in range(10002)]}}
  first=adapter.inspect(json.dumps(obj).encode(),'first.json');self.assertEqual(len(first['media']),10000)
  other=adapter.inspect(json.dumps({'tracks':[],'materials':{'videos':[{'path':'0.mp4'}]}}).encode(),'second.json');self.assertEqual(len(other['media']),1)
if __name__=='__main__':unittest.main()
