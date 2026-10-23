import unittest,sys,json,gzip,io,zipfile
from pathlib import Path
# Avoid the stdlib inspect name collision in unittest imports by loading explicitly.
import importlib.util
spec=importlib.util.spec_from_file_location('project_adapter',Path(__file__).resolve().parents[1]/'native/inspect.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter);inspect=adapter.inspect
class Projects(unittest.TestCase):
 def test_fcpxml_rational_and_doctype(self):
  p=inspect(b'<?xml version="1.0"?><!DOCTYPE fcpxml><fcpxml><resources><asset id="r1" name="shot" src="media/shot.mp4"/></resources><project name="Demo"><sequence><spine><asset-clip ref="r1" offset="25/25s" duration="50/25s"/></spine></sequence></project></fcpxml>','demo.fcpxml')
  self.assertEqual(p['tracks'][0]['clips'][0]['start'],1);self.assertEqual(p['tracks'][0]['clips'][0]['duration'],2);self.assertEqual(p['media'][0]['status'],'unverified')
 def test_otio_gap(self):
  p=inspect(json.dumps({'OTIO_SCHEMA':'Timeline.1','name':'Test','tracks':{'OTIO_SCHEMA':'Stack.1','children':[{'OTIO_SCHEMA':'Track.1','kind':'Video','children':[{'OTIO_SCHEMA':'Gap.1','source_range':{'duration':{'value':24,'rate':24}}},{'OTIO_SCHEMA':'Clip.2','name':'Shot','source_range':{'duration':{'value':48,'rate':24}},'media_reference':{'target_url':'shot.mp4'}}]}]}}).encode(),'t.otio')
  self.assertEqual(p['tracks'][0]['clips'][1]['start'],1);self.assertEqual(p['tracks'][0]['clips'][1]['duration'],2)
 def test_jianying_hour_microseconds(self):
  p=inspect(json.dumps({'tracks':[{'segments':[{'material_id':'a','target_timerange':{'start':3600000000,'duration':5000000}}]}],'materials':{'videos':[{'id':'a','path':'/private/video.mp4'}]}}).encode(),'draft_content.json')
  self.assertEqual(p['tracks'][0]['clips'][0]['start'],3600);self.assertEqual(p['tracks'][0]['clips'][0]['duration'],5)
 def test_mlt_inclusive_frames_and_blanks(self):
  p=inspect(b'<mlt><profile frame_rate_num="25" frame_rate_den="1"/><producer id="p"><property name="resource">a.mp4</property></producer><playlist id="track"><blank length="25"/><entry producer="p" in="10" out="59"/></playlist></mlt>','t.mlt')
  self.assertEqual(p['tracks'][0]['clips'][0]['start'],1);self.assertEqual(p['tracks'][0]['clips'][0]['duration'],2)
 def test_premiere_gzip(self):
  p=inspect(gzip.compress(b'<PremiereData><Sequence ObjectID="42"><Name>Main</Name></Sequence><FilePath>C:\\clips\\one.mov</FilePath></PremiereData>'),'demo.prproj');self.assertEqual(p['sequences'],['Main']);self.assertEqual(len(p['media']),1);self.assertEqual(p['tracks'],[])
 def test_xmeml(self):
  p=inspect(b'<xmeml><sequence><media><video><track><clipitem><name>Shot</name><rate><timebase>24</timebase></rate><start>24</start><end>72</end><file><pathurl>media/s.mp4</pathurl></file></clipitem></track></video></media></sequence></xmeml>','t.xml');self.assertEqual(p['tracks'][0]['clips'][0]['duration'],2)
 def test_drp_directory_never_extract(self):
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w') as z:z.writestr('../escape.xml','private')
  p=inspect(b.getvalue(),'t.drp');self.assertEqual(p['entries'][0]['name'],'../escape.xml');self.assertFalse(Path('escape.xml').exists());self.assertEqual(p['tracks'],[])
 def test_entity_rejected(self):
  with self.assertRaises(ValueError):inspect(b'<!DOCTYPE fcpxml [<!ENTITY x SYSTEM "file:///etc/passwd">]><fcpxml>&x;</fcpxml>','evil.fcpxml')
 def test_gzip_bomb(self):
  with self.assertRaises(ValueError):inspect(gzip.compress(b'a'*(16*1024*1024+1)),'bomb.prproj')
 def test_unknown_json(self):
  with self.assertRaisesRegex(ValueError,'不是已支持'):inspect(b'{"private":1}','settings.json')
 def test_binary_guidance(self):
  with self.assertRaises(ValueError):inspect(b'RIFFbinary','a.aep')
 def test_malformed(self):
  with self.assertRaises(Exception):inspect(b'<mlt><broken>','a.mlt')
if __name__=='__main__':unittest.main()
