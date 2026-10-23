import sys,time,pathlib,subprocess,json,resource,os,signal,tempfile
D,E=map(pathlib.Path,sys.argv[1:]);started=time.monotonic();proc=None

def status(**x):(D/'status').write_text(json.dumps(x))
def limit():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_FSIZE,(82*1024**2,82*1024**2))
def run(args,timeout):
 global proc
 out_file=tempfile.TemporaryFile();err_file=tempfile.TemporaryFile()
 proc=subprocess.Popen(args,stdout=out_file,stderr=err_file,preexec_fn=limit,start_new_session=True)
 end=time.monotonic()+timeout
 while proc.poll() is None:
  if time.monotonic()>end or time.time()-D.stat().st_mtime>40 or (D/'cancel').exists():
   os.killpg(proc.pid,signal.SIGKILL);proc.wait();out_file.close();err_file.close();raise ValueError('视频会话已取消、失去连接或超时')
  time.sleep(.2)
 proc.wait();out_file.seek(0);err_file.seek(0);out=out_file.read(1048577);err=err_file.read(1048576);out_file.close();err_file.close()
 if len(out)>1048576:raise ValueError('媒体信息超过预览限制')
 if proc.returncode:raise ValueError(err.decode(errors='replace')[-700:] or '媒体处理失败')
 return out
try:
 while not (D/'started').exists():
  if time.monotonic()-started>900 or (D/'cancel').exists() or time.time()-D.stat().st_mtime>40:raise ValueError('视频上传已取消或超时')
  time.sleep(.2)
 status(state='probing')
 info=json.loads(run([str(E/'bin/ffprobe'),'-v','error','-protocol_whitelist','file,pipe','-show_format','-show_streams','-of','json',str(D/'input')],20))
 streams=[s for s in info.get('streams',[]) if s.get('codec_type')=='video']
 if not streams:raise ValueError('没有视频轨道')
 if int(streams[0].get('width',0))*int(streams[0].get('height',0))>8192**2:raise ValueError('视频分辨率超出预览限制')
 status(state='transcoding',media=info)
 args=[str(E/'bin/ffmpeg'),'-hide_banner','-loglevel','error','-nostdin','-threads','1','-filter_threads','1','-protocol_whitelist','file,pipe','-i',str(D/'input'),'-map','0:v:0','-map','0:a:0?','-sn','-dn','-vf','scale=w=min(1280\\,iw):h=min(720\\,ih):force_original_aspect_ratio=decrease:force_divisible_by=2','-t','300','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-b:v','1400k','-maxrate','1800k','-bufsize','3600k','-threads','1','-c:a','aac','-b:a','96k','-movflags','+faststart','-fs',str(80*1048576),'-y',str(D/'preview.mp4')]
 run(args,600);status(state='ready',media=info,notice='兼容预览副本 · 最多 720p / 前 5 分钟；非原始画质，HDR 色彩可能变化。')
except Exception as e:status(state='error',error=str(e)[:900])
finally:
 if proc and proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
 (D/'input').unlink(missing_ok=True);(D/'done').touch()
