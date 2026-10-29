const {app,BrowserWindow}=require('electron');
const fs=require('node:fs');
const out=process.argv.find(s=>s.startsWith('--validation-output='))?.slice('--validation-output='.length);
if(!out)throw Error('Missing output path');
const events=[];app.on('child-process-gone',(_,d)=>events.push(d));
const timer=setTimeout(()=>{fs.writeFileSync(out,JSON.stringify({error:'Timed out',events}));app.exit(1)},60000);
app.whenReady().then(async()=>{
 const win=new BrowserWindow({width:900,height:650,webPreferences:{sandbox:true}});
 await win.loadURL('data:text/html,<html><body style="background:linear-gradient(45deg,%23254,%235ad);font:20px Arial"><h1>Electron 45 GPU check</h1><input type="range"><canvas id="c" width="32" height="32"></canvas></body></html>');
 await new Promise(r=>setTimeout(r,10000));
 const draw=await win.webContents.executeJavaScript(`(()=>{const g=document.querySelector('#c').getContext('webgl');if(!g)return {error:'WebGL unavailable'};g.clearColor(.2,.4,.8,1);g.clear(g.COLOR_BUFFER_BIT);const p=new Uint8Array(4);g.readPixels(0,0,1,1,g.RGBA,g.UNSIGNED_BYTE,p);const c=document.createElement('canvas');const g2=c.getContext('webgl2');return {pixels:[...p],error:g.getError(),version:g.getParameter(g.VERSION),webgl2Available:!!g2}})()`);
 const gpu=await app.getGPUInfo('complete').catch(e=>({error:String(e)}));
 fs.writeFileSync(out,JSON.stringify({versions:process.versions,argv:process.argv,gpu,features:app.getGPUFeatureStatus(),draw,events},null,2));
 clearTimeout(timer);app.exit(draw.error===0?0:1);
}).catch(e=>{fs.writeFileSync(out,JSON.stringify({error:String(e),events}));clearTimeout(timer);app.exit(1)});
