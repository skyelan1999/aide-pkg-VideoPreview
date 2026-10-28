#!/usr/bin/env python3
"""Bounded read-only project adapters. Never follows referenced paths or extracts archives."""
import sys,json,gzip,io,zipfile,re,xml.etree.ElementTree as ET
from fractions import Fraction
MAX=16*1024*1024

def seconds(value):
 try:
  s=str(value).strip().removesuffix('s')
  n=float(Fraction(s))
  return n if 0<=n<315360000 else None
 except (ValueError,ZeroDivisionError,OverflowError):return None

def inspect(data,name):
 if len(data)>MAX:raise ValueError('工程超过 16 MiB 限制')
 out={'format':'','name':name.rsplit('/',1)[-1], 'tracks':[], 'media':[], 'warnings':[], 'sequences':[]}
 media_paths=set()
 def media(p,label=''):
  if not isinstance(p,str) or not p.strip():return
  if len(out['media'])>=10000:return
  if p not in media_paths:
   media_paths.add(p)
   out['media'].append({'name':label or re.split(r'[/\\]',p)[-1],'path':p,'status':'unverified'})
 def track(label,clips,kind='video'):
  if len(out['tracks'])<128:out['tracks'].append({'name':label,'kind':kind,'clips':clips[:2000]})
 def clip(label,start=None,duration=None,source=''):
  return {'name':str(label)[:512],'start':start,'duration':duration,'source':str(source)[:4096]}
 if data.startswith(b'\x1f\x8b'):
  with gzip.GzipFile(fileobj=io.BytesIO(data)) as f:data=f.read(MAX+1)
  if len(data)>MAX:raise ValueError('解压后的工程超过 16 MiB')
 if data.startswith(b'PK'):
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   entries=z.infolist()
   if len(entries)>2000 or sum(e.file_size for e in entries)>128*1024*1024:raise ValueError('工程归档过大')
   out['format']='DaVinci Resolve archive' if name.lower().endswith('.drp') else 'Project archive'
   out['entries']=[{'name':e.filename,'size':e.file_size} for e in entries[:300]]
   out['warnings'].append('归档已识别；此版本仅查看目录，不解码 Resolve 私有时间线，也不解压或运行工程。')
   return out
 text=data.decode('utf-8-sig')
 if text.lstrip().startswith('{'):
  obj=json.loads(text)
  if obj.get('OTIO_SCHEMA','').startswith(('Timeline.','SerializableCollection.')):
   out['format']='OpenTimelineIO'
   def walk(node):
    if not isinstance(node,dict):return
    schema=node.get('OTIO_SCHEMA','')
    if schema.startswith('Track.'):
     clips=[];cursor=0
     for c in node.get('children',[]):
      sr=c.get('source_range') or {};d=sr.get('duration') or {};dur=seconds(d.get('value',0));rate=seconds(d.get('rate',1));dur=dur/rate if dur is not None and rate else None
      refs=c.get('media_references') or {};ref=c.get('media_reference') or refs.get(c.get('active_media_reference_key','DEFAULT_MEDIA')) or {};p=ref.get('target_url','');media(p,c.get('name',''))
      if c.get('OTIO_SCHEMA','').startswith('Transition.'):
       out['warnings'].append('转场仅列出索引，不占用顺序时间；未合成转场画面。');dur=0
      if c.get('effects') or c.get('OTIO_SCHEMA','').startswith('Stack.'):
       out['warnings'].append('存在嵌套或速度/效果；索引不代表精确合成时间线。')
      clips.append(clip(c.get('name') or c.get('OTIO_SCHEMA','clip'),cursor,dur,p));cursor+=dur or 0
     track(node.get('name') or 'Track',clips,node.get('kind','Video').lower())
    for key in ('tracks','children'):
     v=node.get(key)
     if isinstance(v,dict):walk(v)
     elif isinstance(v,list):
      for item in v:walk(item)
   walk(obj);out['sequences'].append(obj.get('name','Timeline'))
  elif isinstance(obj.get('tracks'),list) and isinstance(obj.get('materials'),dict):
   out['format']='剪映 / CapCut draft'
   lookup={}
   for items in obj['materials'].values():
    if not isinstance(items,list):continue
    for m in items:
     if isinstance(m,dict):lookup[m.get('id','')]=m;media(m.get('path',''),m.get('material_name',''))
   for i,t in enumerate(obj['tracks']):
    clips=[]
    for c in t.get('segments',[]):
     m=lookup.get(c.get('material_id'),{});r=c.get('target_timerange') or {}
     a=seconds(Fraction(str(r.get('start',0)))/1000000);d=seconds(Fraction(str(r.get('duration',0)))/1000000)
     clips.append(clip(m.get('material_name') or m.get('path') or c.get('id','片段'),a,d,m.get('path','')))
    track(t.get('name') or f'轨道 {i+1}',clips,t.get('type','video'))
  else:raise ValueError('该 JSON 不是已支持的剪辑工程；请使用 Aide 原生查看器。')
 elif text.lstrip().startswith('<'):
  text=re.sub(r'<!DOCTYPE\s+fcpxml\s*>','',text,flags=re.I)
  if re.search(r'<!\s*(DOCTYPE|ENTITY)',text,re.I):raise ValueError('不支持含 DTD/外部实体的 XML 工程')
  root=ET.fromstring(text)
  elements=list(root.iter())
  if len(elements)>100000:raise ValueError('工程节点过多')
  for e in elements:e.tag=e.tag.rsplit('}',1)[-1]
  if root.tag=='fcpxml':
   out['format']='Final Cut Pro XML';assets={}
   for a in root.findall('.//asset'):
    rep=a.find('media-rep');p=a.get('src') or (rep.get('src','') if rep is not None else '')
    assets[a.get('id','')]={'path':p,'name':a.get('name','')};media(p,a.get('name',''))
   lanes={}
   for e in root.iter():
    if e.tag in ('asset-clip','clip','ref-clip','gap'):
     a=assets.get(e.get('ref'),{});lane=e.get('lane','0');lanes.setdefault(lane,[]).append(clip(e.get('name') or a.get('name') or e.tag,seconds(e.get('offset')),seconds(e.get('duration')),a.get('path','')))
   for lane,clips in lanes.items():track('Lane '+lane,clips,'audio' if lane.startswith('-') else 'video')
   out['sequences']=[p.get('name','Project') for p in root.findall('.//project')]
   out['warnings'].append('显示源 XML 的 lane/offset；嵌套片段、复合片段和速度变化未展开，不能视为精确扁平化时间线。')
  elif root.tag in ('mlt','kdenlive'):
   out['format']='Kdenlive / MLT';producers={}
   for p in root.findall('.//producer')+root.findall('.//chain'):
    props={x.get('name'):x.text or '' for x in p.findall('property')};src=props.get('resource','');producers[p.get('id')]=src;media(src)
   profile=root.find('profile');fps=25
   if profile is not None:
    try:fps=float(profile.get('frame_rate_num','25'))/float(profile.get('frame_rate_den','1'))
    except (ValueError,ZeroDivisionError):pass
   def mlt_time(v):
    if not v:return None
    if ':' in v:
     try:
      h,m,s=v.split(':');return int(h)*3600+int(m)*60+float(s)
     except ValueError:return None
    n=seconds(v);return n/fps if n is not None else None
   for i,p in enumerate(root.findall('.//playlist')):
    clips=[];cursor=0
    for e in p:
     if e.tag=='blank':cursor+=mlt_time(e.get('length')) or 0
     if e.tag!='entry':continue
     start=mlt_time(e.get('in'));end=mlt_time(e.get('out'));dur=end-start+1/fps if end is not None and start is not None else None;src=producers.get(e.get('producer'),'')
     clips.append(clip(src or e.get('producer','Clip'),cursor,dur,src));cursor+=dur or 0
    track(p.get('id') or f'Track {i+1}',clips)
  elif root.tag=='xmeml':
   out['format']='Final Cut 7 / Premiere XML'
   for f in root.findall('.//file'):media(f.findtext('pathurl',''),f.findtext('name',''))
   for i,t in enumerate(root.findall('.//track')):
    clips=[]
    for c in t.findall('clipitem'):
     rate=seconds(c.findtext('rate/timebase','25')) or 25;a=seconds(c.findtext('start'));b=seconds(c.findtext('end'));clips.append(clip(c.findtext('name','Clip'),a/rate if a is not None else None,(b-a)/rate if a is not None and b is not None else None,c.findtext('file/pathurl','')))
    track(f'Track {i+1}',clips,'audio' if any(c.find('sourcetrack/mediatype') is not None and c.findtext('sourcetrack/mediatype')=='audio' for c in t.findall('clipitem')) else 'video')
  elif root.tag=='PremiereData':
   out['format']='Premiere Pro project'
   for e in root.iter():
    if e.tag in ('FilePath','ActualMediaFilePath','MediaFilePath'):media(e.text or '')
    if e.tag=='Sequence':out['sequences'].append(e.findtext('Name') or e.get('ObjectID','Sequence'))
   out['warnings'].append('Premiere 私有工程仅索引素材和序列。请导出 Final Cut XML / OTIO 获取可核对时间线；此处不推断私有 tick/引用关系。')
  else:raise ValueError('不支持此 XML 工程结构')
 else:raise ValueError('该工程为二进制或暂未支持；可从剪辑软件导出 FCP XML / OTIO。')
 out['warnings'].append('素材路径仅作索引，尚未验证可访问性；不会自动读取绝对路径、联网或执行特效。')
 return out

if __name__=='__main__':
 try:
  with open(sys.argv[1],'rb') as f:data=f.read(MAX+1)
  print(json.dumps(inspect(data,sys.argv[2]),ensure_ascii=False,allow_nan=False))
 except Exception as e:
  print(json.dumps({'error':str(e)[:400]},ensure_ascii=False));sys.exit(1)
