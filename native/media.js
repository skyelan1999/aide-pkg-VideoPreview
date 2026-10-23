'use strict';
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto'),cp=require('node:child_process');
const ROOT=path.join(os.homedir(),'.cache/aide-video-preview'),ENGINE=path.join(ROOT,'engine'),JOBS=path.join(ROOT,'media'),LIMIT=128*1048576,CHUNK=48*1024;
const readJSON=(p,fallback={})=>{try{return JSON.parse(fs.readFileSync(p,'utf8'));}catch(_){return fallback;}};
function dir(id){if(!/^[a-f0-9]{48}$/.test(id||''))throw Error('Invalid media session');const d=path.join(JOBS,id),s=fs.lstatSync(d);if(!s.isDirectory()||s.isSymbolicLink())throw Error('Invalid media session');return d;}
function ready(){return fs.existsSync(path.join(ENGINE,'READY'));}
function startProcess(script,args){const p=cp.spawn(script,args,{detached:true,stdio:'ignore'});p.unref();}
function num(n,max){if(!Number.isSafeInteger(n)||n<0||n>max)throw Error('Invalid range');return n;}
async function io(a){
 fs.mkdirSync(JOBS,{recursive:true,mode:0o700});
 if(a.action==='engine-status')return{ready:ready(),...readJSON(path.join(ROOT,'install-status.json'),{state:'not-installed'})};
 if(a.action==='engine-install'){
  if(a.confirm!==true)throw Error('请明确点击安装兼容引擎');if(ready())return{ready:true,state:'ready'};
  const lock=path.join(ROOT,'install.lock');try{fs.mkdirSync(lock);}catch(e){if(Date.now()-fs.statSync(lock).mtimeMs<1800000)return{state:'installing'};fs.rmdirSync(lock);fs.mkdirSync(lock);}
  fs.writeFileSync(path.join(ROOT,'install-status.json'),JSON.stringify({state:'installing',bytes:0}));startProcess(process.execPath,[path.join(__dirname,'engine-install.js'),ROOT]);return{state:'installing'};
 }
 if(a.action==='media-begin'){
  if(!ready())throw Error('请先安装兼容引擎');num(a.size,LIMIT);if(!a.size)throw Error('Empty video');
  const lock=path.join(JOBS,'admission');try{fs.mkdirSync(lock);}catch(_){if(Date.now()-fs.statSync(lock).mtimeMs>10000){fs.rmdirSync(lock);fs.mkdirSync(lock);}else throw Error('另一个视频会话正在建立');}
  try{
   for(const n of fs.readdirSync(JOBS)){if(!/^[a-f0-9]{48}$/.test(n))continue;const d=path.join(JOBS,n);if(Date.now()-fs.statSync(d).mtimeMs>120000){fs.writeFileSync(path.join(d,'cancel'),'');if(fs.existsSync(path.join(d,'done')))fs.rmSync(d,{recursive:true,force:true});}else if(!fs.existsSync(path.join(d,'done')))throw Error('已有视频正在转换，请等待或取消');}
   const completed=fs.readdirSync(JOBS).filter(n=>/^[a-f0-9]{48}$/.test(n)&&fs.existsSync(path.join(JOBS,n,'done'))).sort((a,b)=>fs.statSync(path.join(JOBS,a)).mtimeMs-fs.statSync(path.join(JOBS,b)).mtimeMs);while(completed.length>=3)fs.rmSync(path.join(JOBS,completed.shift()),{recursive:true,force:true});
   const id=crypto.randomBytes(24).toString('hex'),d=path.join(JOBS,id);fs.mkdirSync(d,{mode:0o700});fs.writeFileSync(path.join(d,'meta'),JSON.stringify({size:a.size}));fs.writeFileSync(path.join(d,'input'),'');startProcess('python3',[path.join(__dirname,'media-worker.py'),d,ENGINE]);return{id};
  }finally{fs.rmdirSync(lock);}
 }
 const d=dir(a.id);fs.utimesSync(d,new Date(),new Date());
 if(a.action==='media-cancel'){fs.writeFileSync(path.join(d,'cancel'),'');return{cancelled:true};}
 if(a.action==='media-write'){
  if(fs.existsSync(path.join(d,'started'))||fs.existsSync(path.join(d,'done')))throw Error('Upload closed');
  if(typeof a.data!=='string'||a.data.length>CHUNK*4/3||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(a.data))throw Error('Invalid media chunk');
  const b=Buffer.from(a.data,'base64'),file=path.join(d,'input'),size=readJSON(path.join(d,'meta')).size;num(a.offset,LIMIT);if(!b.length||a.offset!==fs.statSync(file).size||a.offset+b.length>size)throw Error('Invalid media offset');fs.appendFileSync(file,b);return{offset:a.offset+b.length};
 }
 if(a.action==='media-start'){if(fs.statSync(path.join(d,'input')).size!==readJSON(path.join(d,'meta')).size)throw Error('Incomplete video');fs.closeSync(fs.openSync(path.join(d,'started'),'wx'));return{started:true};}
 if(a.action==='media-read'){
  const state=readJSON(path.join(d,'status'),{state:'waiting'}),done=fs.existsSync(path.join(d,'done'));if(state.error)return{...state,done};
  if(!done)return{...state,done:false};
  const file=path.join(d,'preview.mp4'),size=fs.statSync(file).size,offset=num(a.offset||0,80*1048576);if(offset>size)throw Error('Invalid preview range');const b=Buffer.alloc(Math.min(CHUNK,size-offset)),fd=fs.openSync(file,'r');try{fs.readSync(fd,b,0,b.length,offset);}finally{fs.closeSync(fd);}return{...state,done:true,data:b.toString('base64'),offset:offset+b.length,size};
 }
 throw Error('Unknown media action');
}
module.exports={io};
