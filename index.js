'use strict';
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto'),cp=require('node:child_process');
const ROOT=path.join(os.homedir(),'.cache','aide-video-preview'),LIMIT=16*1048576,CHUNK=48*1024;
function init(){fs.mkdirSync(ROOT,{recursive:true,mode:0o700});for(const n of fs.readdirSync(ROOT)){if(!/^[a-f0-9]{48}$/.test(n))continue;const p=path.join(ROOT,n);if(Date.now()-fs.lstatSync(p).mtimeMs>300000)fs.rmSync(p,{force:true,recursive:true});}}
function dir(id){if(!/^[a-f0-9]{48}$/.test(id||''))throw Error('Invalid session');const d=path.join(ROOT,id);if(!fs.lstatSync(d).isDirectory()||fs.lstatSync(d).isSymbolicLink())throw Error('Invalid session');return d;}
function integer(n,max){if(!Number.isSafeInteger(n)||n<0||n>max)throw Error('Invalid range');return n;}
function io(a){
 if(a.action?.startsWith('engine-')||a.action?.startsWith('media-'))return require('./native/media.js').io(a);
 init();if(a.action==='begin'){
  integer(a.size,LIMIT);if(!a.size)throw Error('Empty project');
  if(fs.readdirSync(ROOT).filter(n=>/^[a-f0-9]{48}$/.test(n)).length>=4)throw Error('已有多个工程正在读取，请关闭后重试');
  const id=crypto.randomBytes(24).toString('hex'),d=path.join(ROOT,id);fs.mkdirSync(d,{mode:0o700});fs.writeFileSync(path.join(d,'meta'),JSON.stringify({size:a.size,name:typeof a.name==='string'?a.name.slice(0,256):'project'}));fs.writeFileSync(path.join(d,'input'),'');return{id};
 }
 const d=dir(a.id);fs.utimesSync(d,new Date(),new Date());
 if(a.action==='cancel'){fs.rmSync(d,{recursive:true,force:true});return{cancelled:true};}
 if(a.action==='write'){
  if(typeof a.data!=='string'||a.data.length>CHUNK*4/3||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(a.data))throw Error('Invalid chunk');
  const offset=integer(a.offset,LIMIT),meta=JSON.parse(fs.readFileSync(path.join(d,'meta'))),file=path.join(d,'input'),b=Buffer.from(a.data,'base64');
  if(!b.length||fs.statSync(file).size!==offset||offset+b.length>meta.size)throw Error('Invalid upload offset');fs.appendFileSync(file,b);return{offset:offset+b.length};
 }
 if(a.action==='inspect'){
  const meta=JSON.parse(fs.readFileSync(path.join(d,'meta'))),file=path.join(d,'input');if(fs.statSync(file).size!==meta.size)throw Error('Incomplete project');
  try{return JSON.parse(cp.execFileSync('python3',[path.join(__dirname,'native/inspect.py'),file,meta.name],{timeout:12000,maxBuffer:2*1048576,encoding:'utf8'}));}
  catch(e){let message='工程解析失败';try{message=JSON.parse(String(e.stdout)).error||message;}catch(_){}throw Error(message);}
  finally{fs.rmSync(d,{recursive:true,force:true});}
 }
 throw Error('Unknown action');
}
module.exports={name:'video-preview',apply(ctx){ctx.tool({name:'video_preview_io',description:'只读、限量解析当前绑定的剪辑工程。素材路径仅索引，不会执行工程或访问素材地址。',parameters:{type:'object',properties:{action:{type:'string',enum:['begin','write','inspect','cancel','engine-status','engine-install','media-begin','media-write','media-start','media-read','media-cancel']},id:{type:'string'},confirm:{type:'boolean'},name:{type:'string'},size:{type:'integer'},offset:{type:'integer'},data:{type:'string'}},required:['action'],additionalProperties:false},handler:io});}};
