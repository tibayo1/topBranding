/* Shared Rhythm: a procedural dimensional motion study. Original parish contours
   are used as the source surfaces; the final endorsement/name comes from15. */
const W=1920,H=1080,canvas=document.getElementById('stage'),ctx=canvas.getContext('2d');
canvas.width=W;canvas.height=H;
const PI=Math.PI,TAU=PI*2;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const mix=(a,b,u)=>a+(b-a)*u;
const smooth=(a,b,t)=>{const q=clamp((t-a)/(b-a));return q*q*(3-2*q)};
const smoother=(a,b,t)=>{const q=clamp((t-a)/(b-a));return q*q*q*(q*(q*6-15)+10)};
const rgba=(v,a=1)=>`rgba(${v[0]|0},${v[1]|0},${v[2]|0},${a})`;
const C={teal:[16,73,76],night:[5,23,29],ivory:[246,243,236],gold:[182,146,85],sand:[217,203,180]};
const lerpColor=(a,b,u)=>a.map((v,i)=>mix(v,b[i],u));
const P=[[[16,132],[69,103],[65,217],[16,207]],[[67,95],[122,65],[118,167],[85,176],[81,97]],[[133,45],[173,18],[169,176],[137,167]],[[184,105],[240,138],[240,217],[188,199]]];
const heights=[90,111,158,112];
function load(src){return new Promise((r,j)=>{const im=new Image();im.onload=()=>r(im);im.onerror=j;im.src=src})}
const assetReady=Promise.all([load(ASSETS.end),load(ASSETS.overlay),load(ASSETS.symbol)]).then(([end,overlay,symbol])=>({end,overlay,symbol}));
function stage(t){
 const resolve=smoother(8.35,9.45,t),wide=smoother(1.3,8.3,t);
 return {cx:mix(mix(1100,960,wide),1264.85,resolve),cy:mix(mix(230,440,wide),453.004523,resolve),
   scale:mix(mix(5.9,3.05,wide),1.3718592966,resolve),yaw:mix(mix(-.53,-.15,wide),0,resolve),pitch:mix(mix(.30,.065,wide),0,resolve),resolve};
}
function world(x,y,z,t){
 const s=stage(t),a=s.yaw,b=s.pitch;let px=x-128,py=y-128,pz=z;
 const xx=px*Math.cos(a)+pz*Math.sin(a),zz=-px*Math.sin(a)+pz*Math.cos(a);
 const yy=py*Math.cos(b)-zz*Math.sin(b),z2=py*Math.sin(b)+zz*Math.cos(b);
 const perspective=850/(850+z2);
 return [s.cx+xx*s.scale*perspective,s.cy+yy*s.scale*perspective,z2];
}
function polygon(points){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath()}
function panelPoint(x,y,i,t,back=0){
 const lift=smoother(3.25+i*.24,7.4+i*.17,t),flat=smoother(7.8,9.4,t);
 const angle=mix(1.45,0,lift),yaw=(i%2?-.42:.38)*(1-flat)*(1-lift*.7),pivot=[42,98,153,213][i];
 const dy=y-217,xx=(x-pivot)*Math.cos(yaw),zz=(x-pivot)*Math.sin(yaw);
 let py=217+dy*Math.cos(angle),pz=dy*Math.sin(angle)+zz+back;
 py+=mix(24,0,smoother(4.8,8.2,t));
 return world(pivot+xx,py,pz,t);
}
function bg(t){
 const r=smoother(8.2,10.5,t),base=lerpColor(C.night,C.teal,r);
 ctx.fillStyle=rgba(base);ctx.fillRect(0,0,W,H);
 const light=1-r;
 if(light>0){
  let g=ctx.createRadialGradient(1050,450,10,1050,450,1100);
  g.addColorStop(0,`rgba(19,98,100,${.46*light})`);g.addColorStop(.56,`rgba(11,58,63,${.22*light})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  g=ctx.createRadialGradient(600,290,20,600,290,650);g.addColorStop(0,`rgba(182,146,85,${.052*light})`);g.addColorStop(1,'rgba(182,146,85,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // Soft architectural floor; no horizon or imposed church imagery.
  g=ctx.createRadialGradient(995,860,20,995,860,760);g.addColorStop(0,`rgba(41,95,93,${.17*light})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.save();ctx.translate(0,690);ctx.scale(1,.23);ctx.fillStyle=g;ctx.fillRect(0,-3000,W,6000);ctx.restore();
 }
}
function intersect(poly,x){const ys=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length];if((x>=Math.min(a[0],b[0]))&&(x<=Math.max(a[0],b[0]))&&a[0]!==b[0])ys.push(a[1]+(x-a[0])/(b[0]-a[0])*(b[1]-a[1]))}return [Math.min(...ys),Math.max(...ys)]}
function bezier(a,b,c,d,u){const v=1-u;return a.map((_,i)=>v*v*v*a[i]+3*v*v*u*b[i]+3*v*u*u*c[i]+u*u*u*d[i])}
function strands(t){
 const enter=smoother(0,3.8,t),gather=smoother(1.1,4.8,t),rise=smoother(3.6,7.2,t),out=1-smoother(5.8,7.15,t);
 if(out<.001)return;
 for(let i=0;i<48;i++){
  const group=i%4,j=(i/4)|0,n=(j+.5)/12,poly=P[group],xs=poly.map(p=>p[0]);
  const x=mix(Math.min(...xs)+2,Math.max(...xs)-2,n),[top,bottom]=intersect(poly,x),phase=i*.618;
  const visibility=smoother(.02+group*.43+j*.085,.65+group*.43+j*.085,t)*out;
  if(visibility<.001)continue;
  const direction=i%2?-1:1;
  let points=[];
  const head=clamp((t+.1-group*.18-j*.019)/.75),tail=clamp(head-.95);
  for(let k=0;k<=64;k++){
   const u=mix(tail,head,k/64),gate=smoother(0,1,u);
   const a=[128+direction*(mix(330,270,gather)+j*mix(11,7,gather)),mix(80,120,gather)+Math.sin(phase)*15,-30+j*5];
   const b=[128+direction*(mix(210,160,gather)+j*2),mix(175,205,gather)+Math.cos(phase)*35,-90-j*2];
   const c=[128+direction*(mix(25,15,gather)+group*7),mix(165,185,gather)+Math.sin(phase)*20,-70];
   const d=[x,bottom-3,group*2];
   const free=bezier(a,b,c,d,u);
   const liftY=mix(bottom,top+1,smoother(0,1,u));
   const pl=panelPoint(x,liftY,group,t);
   const p=world(free[0],free[1],free[2],t);
   const blend=rise*Math.pow(gate,.42);
   points.push([mix(p[0],pl[0],blend),mix(p[1],pl[1],blend)]);
  }
  // A small family of unequal voices, not a bar chart or particle shower.
  ctx.beginPath();points.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));
  const primary=j===0;
  ctx.lineCap='round';
  if(primary){
   const a=points[0],b=points[points.length-1],g=ctx.createLinearGradient(a[0],a[1],b[0],b[1]);
   g.addColorStop(0,rgba(C.gold,visibility*.15));g.addColorStop(.45,rgba(C.sand,visibility*.75));g.addColorStop(1,rgba(C.ivory,visibility*.92));
   const upper=[],lower=[];
   points.forEach((p,k)=>{
    const before=points[Math.max(0,k-1)],after=points[Math.min(points.length-1,k+1)],dx=after[0]-before[0],dy=after[1]-before[1],len=Math.hypot(dx,dy)||1;
    const width=mix(43,5,rise)*Math.pow(Math.sin(PI*(k+1)/(points.length+1)),.6)/2;
    upper.push([p[0]-dy/len*width,p[1]+dx/len*width]);lower.push([p[0]+dy/len*width,p[1]-dx/len*width]);
   });
   polygon([...upper,...lower.reverse()]);ctx.fillStyle=g;ctx.fill();
   ctx.beginPath();upper.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));ctx.strokeStyle=rgba(C.ivory,visibility*.72);ctx.lineWidth=1.25;ctx.stroke();
  }else{
   ctx.strokeStyle=rgba(i%5===0?C.gold:C.ivory,visibility*(i%3===0?.40:.17));ctx.lineWidth=i%5===0?1.8:.8;ctx.stroke();
  }
 }
}
function drawPanels(t){
 const reveal=smoother(3.4,6.5,t),flat=smoother(7.7,9.4,t);
 if(reveal<.001)return;
 // Draw backwards according to current depth, preserving true planar contours.
 const faces=P.map((poly,i)=>({poly,i,points:poly.map(p=>panelPoint(...p,i,t))})).sort((a,b)=>b.points.reduce((s,p)=>s+p[2],0)/b.points.length-a.points.reduce((s,p)=>s+p[2],0)/a.points.length);
 for(const {poly,i,points} of faces){
  const alpha=smoother(3.2+i*.24,5.5+i*.20,t);
  if(alpha<.001)continue;
  ctx.save();ctx.globalAlpha=alpha;
  const depth=4.2*(1-flat);
  if(depth>.01){
   const rear=poly.map(p=>panelPoint(...p,i,t,depth));
   for(let e=0;e<points.length;e++){
    const next=(e+1)%points.length;polygon([points[e],points[next],rear[next],rear[e]]);ctx.fillStyle=rgba(lerpColor([58,67,62],C.gold,.34));ctx.fill();
   }
  }
  const bb={x0:Math.min(...points.map(p=>p[0])),x1:Math.max(...points.map(p=>p[0])),y0:Math.min(...points.map(p=>p[1])),y1:Math.max(...points.map(p=>p[1]))};
  let g=ctx.createLinearGradient(bb.x0,bb.y0,bb.x1,bb.y1);
  const shaded=lerpColor([178+i*7,184+i*5,166+i*6],C.ivory,flat);
  const high=lerpColor([252,244,220],C.ivory,flat);
  g.addColorStop(0,rgba(high));g.addColorStop(.42,rgba(lerpColor(shaded,high,.65)));g.addColorStop(1,rgba(shaded));
  polygon(points);ctx.fillStyle=g;ctx.fill();
  // Warm grazing rim and a subtle longitudinal material grain.
  if(flat<.999){
   ctx.save();polygon(points);ctx.clip();
   const rim=ctx.createLinearGradient(bb.x0,0,bb.x1,0);rim.addColorStop(0,`rgba(255,236,185,${.32*(1-flat)})`);rim.addColorStop(.06,'rgba(255,236,185,0)');rim.addColorStop(.9,'rgba(0,0,0,0)');rim.addColorStop(1,`rgba(22,39,39,${.22*(1-flat)})`);ctx.fillStyle=rim;ctx.fillRect(bb.x0,bb.y0,bb.x1-bb.x0,bb.y1-bb.y0);
   const sweep=smoother(4.5+i*.18,6.8+i*.12,t),px=mix(bb.x0-90,bb.x1+90,sweep),sg=ctx.createLinearGradient(px-75,bb.y0,px+75,bb.y1);
   sg.addColorStop(0,'rgba(255,249,226,0)');sg.addColorStop(.48,`rgba(255,249,226,${.20*(1-flat)*Math.sin(PI*sweep)})`);sg.addColorStop(1,'rgba(255,249,226,0)');ctx.fillStyle=sg;ctx.fillRect(bb.x0,bb.y0,bb.x1-bb.x0,bb.y1-bb.y0);
   ctx.restore();
   ctx.beginPath();points.forEach((p,k)=>k?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.strokeStyle=rgba(C.ivory,.24*(1-flat));ctx.lineWidth=.75;ctx.stroke();
  }
  ctx.restore();
 }
}
async function renderFrame(t){
 const images=await assetReady;t=clamp(t,0,14);
 if(t>=10.5){ctx.drawImage(images.end,0,0);return canvas.toDataURL('image/png').split(',')[1]}
 bg(t);
 strands(t);
 if(t<9.4)drawPanels(t);else ctx.drawImage(images.symbol,0,0);
 const resolve=smoother(9.35,10.5,t);
 if(resolve>0){ctx.save();ctx.globalAlpha=resolve;ctx.drawImage(images.overlay,0,0);ctx.restore()}
 if(t<9.35){ctx.fillStyle=`rgba(246,243,236,${.48*(1-smooth(8.8,9.35,t))})`;ctx.font='18px Arial, sans-serif';ctx.fillText('DRAFT — NOT FOR PUBLICATION',72,1014)}
 return canvas.toDataURL('image/png').split(',')[1];
}
window.renderFrame=renderFrame;
let token=0,playing=false;const reduce=document.getElementById('reduce');reduce.checked=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.getElementById('play').onclick=()=>{if(reduce.checked)return;const own=++token;playing=true;const started=performance.now();async function tick(now){if(token!==own)return;const t=Math.min(14,(now-started)/1000);await renderFrame(t);document.getElementById('time').textContent=t.toFixed(1)+' / 14.0 s';if(t<14&&token===own)requestAnimationFrame(tick);else{playing=false;document.getElementById('play').textContent='Replay'}}document.getElementById('play').textContent='Playing';requestAnimationFrame(tick)};
reduce.onchange=async()=>{++token;playing=false;await renderFrame(reduce.checked?14:0);document.getElementById('play').textContent='Play';document.getElementById('time').textContent=reduce.checked?'Still preview':'0.0 / 14.0 s'};
assetReady.then(()=>renderFrame(reduce.checked?14:0));
