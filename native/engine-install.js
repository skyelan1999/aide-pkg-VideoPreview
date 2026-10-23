'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const ROOT=process.argv[2],status=path.join(ROOT,'install-status.json'),entry=require('../runtime/catalog.json')[process.platform+'-'+process.arch];
let bytes=0;const report=x=>{const p=status+'.tmp';fs.writeFileSync(p,JSON.stringify({bytes,...x}));fs.renameSync(p,status);};
(async()=>{let tmp;try{
 if(!entry)throw Error('当前平台无预编译引擎，请使用 Linux ARM64/AMD64 Aide 容器');tmp=fs.mkdtempSync(path.join(ROOT,'install-'));const file=path.join(tmp,'engine.tar.gz'),hash=crypto.createHash('sha256'),fd=fs.openSync(file,'wx');
 try{const r=await fetch(entry.url,{signal:AbortSignal.timeout(1200000)});if(!r.ok)throw Error('引擎下载失败 HTTP '+r.status);for await(const b of r.body){bytes+=b.length;if(bytes>entry.bytes)throw Error('引擎大小超出清单');hash.update(b);fs.writeFileSync(fd,b);report({state:'installing',total:entry.bytes});}}finally{fs.closeSync(fd);}
 if(bytes!==entry.bytes||hash.digest('hex')!==entry.sha256)throw Error('引擎 SHA-256 或大小校验失败');const dest=path.join(tmp,'engine');fs.mkdirSync(dest);cp.execFileSync('python3',[path.join(__dirname,'extract-engine.py'),file,dest],{timeout:30000});
 const ffmpeg=path.join(dest,'bin/ffmpeg');const version=cp.execFileSync(ffmpeg,['-version'],{timeout:10000,encoding:'utf8'});if(!version.includes('9.0.2')||!version.includes('--enable-gpl')||version.includes('--enable-nonfree'))throw Error('引擎身份不符合构建清单');fs.writeFileSync(path.join(dest,'READY'),entry.sha256);fs.renameSync(dest,path.join(ROOT,'engine'));report({state:'ready',ready:true,total:entry.bytes});
 }catch(e){report({state:'error',error:e.message});}finally{if(tmp)fs.rmSync(tmp,{recursive:true,force:true});fs.rmSync(path.join(ROOT,'install.lock'),{recursive:true,force:true});}})();
