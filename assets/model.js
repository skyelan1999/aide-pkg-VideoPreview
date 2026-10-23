'use strict';
(function(root){
 function safeAsset(p){if(typeof p!=='string'||!p||p.length>4096||/^[a-z][a-z\d+.-]*:/i.test(p)||p.startsWith('/')||p.startsWith('\\')||p.includes('\\')||p.split('/').some(x=>!x||x==='.'||x==='..'))return null;return p;}
 function time(n){if(!Number.isFinite(n)||n<0)return '—';const h=Math.floor(n/3600),m=Math.floor(n/60)%60,s=(n%60).toFixed(2).padStart(5,'0');return (h?String(h).padStart(2,'0')+':':'')+String(m).padStart(2,'0')+':'+s;}
 function srtToVtt(text){if(text.length>2*1048576)throw Error('字幕超过 2 MiB');const t=text.replace(/^\uFEFF/,'').replace(/\r\n?/g,'\n');if(t.startsWith('WEBVTT'))return t;if(!/\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->/.test(t))throw Error('请选择 SRT 或 WebVTT 字幕');return 'WEBVTT\n\n'+t.replace(/(\d{2}:\d{2}:\d{2}),(\d{3})/g,'$1.$2');}
 root.VideoModel={safeAsset,time,srtToVtt};if(typeof module==='object')module.exports=root.VideoModel;
})(globalThis);
