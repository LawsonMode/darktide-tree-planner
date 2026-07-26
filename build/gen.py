#!/usr/bin/env python3
import json
data = open('data.json',encoding='utf-8').read()

TEMPLATE = r"""<title>Darktide Skill Trees — All Classes</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{
    --ground:#0d0e10; --panel:#16181c; --panel2:#1d2025; --edge:#2c3037; --edge-on:#4fc9d4;
    --text:#d7dade; --muted:#878d96; --hair:#262a31;
    --gold:#e0b23c; --keymod:#b89a52; --ability:#a583d6; --abilmod:#7d6bb0;
    --blitz:#d98a3d; --aura:#5fb06a; --passive:#3fb0bd; --stat:#7a8089; --root:#c9ccd1; --glow:#5fd6df; --stimm:#a6c34f;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{background:radial-gradient(1200px 600px at 50% -10%, #1a1c20 0%, transparent 60%),var(--ground);
    color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}
  header{flex:0 0 auto;display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:11px 18px;
    background:linear-gradient(180deg,#191b1f,#131519);border-bottom:1px solid var(--hair);box-shadow:0 2px 14px rgba(0,0,0,.5);z-index:20}
  .brand{display:flex;flex-direction:column;gap:2px;min-width:150px}
  .brand .eyebrow{font-size:10px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);opacity:.85}
  .brand h1{font-family:Georgia,"Times New Roman",serif;font-size:19px;font-weight:600;margin:0;letter-spacing:.02em}
  .classbar{display:flex;gap:5px;flex-wrap:wrap}
  .classbar button{font-family:inherit;font-size:12.5px;color:var(--muted);background:var(--panel2);
    border:1px solid var(--hair);border-radius:6px;padding:7px 11px;cursor:pointer;letter-spacing:.02em}
  .classbar button:hover{border-color:var(--gold);color:var(--text)}
  .classbar button.on{background:var(--gold);color:#1a1408;border-color:var(--gold);font-weight:600}
  .controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-left:auto}
  label.ctl{display:flex;flex-direction:column;gap:3px;font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
  button.act,input.name{font-family:inherit;font-size:13px;color:var(--text);background:var(--panel2);border:1px solid var(--hair);border-radius:6px;padding:7px 10px;cursor:pointer}
  button.act:hover{border-color:var(--gold)}
  input.name{width:150px;cursor:text}
  input.name:focus{outline:none;border-color:var(--gold)}
  .primary{background:var(--gold);color:#1a1408;border-color:var(--gold);font-weight:600}
  .primary:hover{filter:brightness(1.08)}
  .zoombar{display:flex;gap:4px}
  .zoombar button{width:32px;padding:6px 0;font-size:15px;line-height:1;font-family:inherit;color:var(--text);background:var(--panel2);border:1px solid var(--hair);border-radius:6px;cursor:pointer}
  .badge{display:flex;flex-direction:column;gap:2px;align-items:flex-end}
  .badge .n{font-family:Georgia,serif;font-size:19px;line-height:1;color:var(--gold);font-variant-numeric:tabular-nums}
  .badge .n.full{color:#cc5a5c}
  .badge .l{font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
  main{flex:1 1 auto;display:flex;min-height:0}
  #stage{position:relative;flex:1 1 auto;min-width:0;overflow:hidden;cursor:grab;background:radial-gradient(900px 900px at 40% 30%, #131519 0%, #0b0c0e 70%)}
  #stage.grab{cursor:grabbing}
  svg{position:absolute;top:0;left:0;transform-origin:0 0}
  .edge{stroke:var(--edge);stroke-width:3}
  .edge.on{stroke:var(--edge-on);stroke-width:4;filter:drop-shadow(0 0 4px var(--glow))}
  .node{cursor:pointer}
  .node .ring{fill:var(--panel);stroke-width:3}
  .node text{font-family:system-ui,sans-serif;fill:var(--text);text-anchor:middle;pointer-events:none;paint-order:stroke;stroke:#000;stroke-width:3px;stroke-linejoin:round}
  .node.locked{opacity:.14}
  .node.locked .art{filter:grayscale(1)}
  .node.avail{opacity:.62}
  .node.avail .ring{stroke-dasharray:5 4}
  .node.active .ring{stroke-width:5;filter:drop-shadow(0 0 8px var(--glow))}
  .node.hot .ring{stroke:#fff !important}
  @keyframes pulse{0%,100%{opacity:.5}50%{opacity:.95}}
  .node.avail:not(.hot){animation:pulse 1.9s ease-in-out infinite}
  @media (prefers-reduced-motion:reduce){.node.avail{animation:none}}
  aside{flex:0 0 330px;max-width:44vw;background:linear-gradient(180deg,#16181c,#101215);border-left:1px solid var(--hair);display:flex;flex-direction:column;overflow:hidden}
  .info{padding:18px;overflow:auto;flex:1 1 auto}
  .info .type{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:6px}
  .info h2{font-family:Georgia,serif;font-size:21px;margin:0 0 10px;line-height:1.15;text-wrap:balance}
  .info p{font-size:14px;line-height:1.55;color:#c3c7cd;margin:0}
  .info .hint{color:var(--muted);font-size:13px;line-height:1.6}
  .summary{border-top:1px solid var(--hair);padding:14px 18px;background:#0f1114}
  .summary h3{margin:0 0 9px;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
  .chip{display:flex;justify-content:space-between;gap:8px;font-size:13px;padding:4px 0;border-bottom:1px dotted #23272e}
  .chip .k{color:var(--muted)} .pts{font-family:Georgia,serif;font-size:15px;color:var(--gold)}
  .legend{display:flex;flex-wrap:wrap;gap:6px 13px;padding:10px 18px;background:#0f1114;border-top:1px solid var(--hair)}
  .legend span{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted)}
  .legend i{width:11px;height:11px;border-radius:50%;display:inline-block}
  .ver{padding:9px 18px 12px;background:#0f1114;border-top:1px solid var(--hair);font-size:10.5px;line-height:1.5;color:#5c626b;letter-spacing:.02em}
  .ver b{color:var(--gold);font-weight:600}
  .toast{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);background:#241a1a;border:1px solid #cc5a5c;color:#f0c9c9;padding:8px 14px;border-radius:7px;font-size:13px;opacity:0;pointer-events:none;transition:opacity .25s;z-index:30}
  .toast.show{opacity:1}
  @media (max-width:860px){aside{position:absolute;right:0;top:0;bottom:0;flex-basis:290px;box-shadow:-8px 0 30px rgba(0,0,0,.6);z-index:15}}
</style>

<header>
  <div class="brand"><span class="eyebrow">Warhammer 40,000 · Darktide</span><h1>Skill Trees</h1></div>
  <div class="classbar" id="classbar"></div>
  <div class="controls">
    <label class="ctl">Build name<input class="name" id="buildName" value="My Build" maxlength="40"></label>
    <button class="act" id="resetBtn" title="Clear all allocated nodes">Reset</button>
    <button class="act primary" id="exportBtn" title="Download this build as a PNG">&#10515; Export PNG</button>
    <div class="badge"><span class="n" id="ptsN">0 / 30</span><span class="l" id="ptsL">Points spent</span></div>
    <div class="zoombar"><button id="zin">+</button><button id="zout">&minus;</button><button id="zfit" style="width:auto;padding:6px 9px;font-size:12px">Fit</button></div>
  </div>
</header>
<main>
  <div id="stage"><svg id="svg"></svg><div class="toast" id="toast"></div></div>
  <aside>
    <div class="info" id="info"><p class="hint"><b>Pick a class above, then click nodes to build.</b> You can only take nodes connected to ones you already have — available nodes pulse. Click an allocated node to remove it (blocked if others route through it). The class node is always on and free. 30 points; one Keystone, Ability, Blitz &amp; Aura each. Hover to read effects. &#10515; exports a PNG.</p></div>
    <div class="summary" id="sum"></div>
    <div class="legend" id="legend"></div>
    <div class="ver" id="ver"></div>
  </aside>
</main>

<script>
/* ===== version / provenance (canonical version spot for this applet) ===== */
const APP_VERSION = '1.0.0';
const GAME_PATCH  = 'Darktide Hotfix 1.12.3 (2026-07-06)';
const DATA_SOURCE = 'Games Lantern';
const DATA_SCRAPED= '2026-07-26';

const DATA = __DATA__;
const ICONS = DATA.icons;
const NS='http://www.w3.org/2000/svg';
let PMAX=30;   // per-class point budget (null = uncapped, e.g. Stimm sub-tree)
const EXCL={keystone:'Keystone',ability:'Ability',blitz:'Blitz',aura:'Aura'};
const CAT={keystone:{c:'var(--gold)',label:'Keystone'},keymod:{c:'var(--keymod)',label:'Keystone mod'},
  ability:{c:'var(--ability)',label:'Ability'},abilmod:{c:'var(--abilmod)',label:'Ability mod'},
  blitz:{c:'var(--blitz)',label:'Blitz (grenade)'},aura:{c:'var(--aura)',label:'Aura'},
  passive:{c:'var(--passive)',label:'Passive'},stat:{c:'var(--stat)',label:'Minor stat'},root:{c:'var(--root)',label:'Class node'},
  stimm:{c:'var(--stimm)',label:'Stimm perk'}};

const svg=document.getElementById('svg'), info=document.getElementById('info'),
      sumEl=document.getElementById('sum'), ptsN=document.getElementById('ptsN'),
      toastEl=document.getElementById('toast');

let CUR, VB, ROOT, active, ADJ, nodeBySlug, nodeEls, edgeEls;

function radius(cat){return cat==='keystone'?36:(cat==='ability'||cat==='blitz'||cat==='aura'||cat==='root')?30:(cat==='stat'?12:24);}
function nearest(x,y){let best=null,bd=1e9;for(const n of CUR.nodes){const d=(n.x-x)**2+(n.y-y)**2;if(d<bd){bd=d;best=n;}}return bd<=1600?best:null;}

function buildClass(key){
  CUR=DATA.classes.find(c=>c.key===key);
  PMAX=(CUR.budget===undefined?30:CUR.budget);
  svg.innerHTML=''; nodeEls={}; edgeEls=[]; nodeBySlug={}; ADJ={};
  CUR.nodes.forEach(n=>{nodeBySlug[n.s]=n; ADJ[n.s]=new Set();});
  VB={x:CUR.viewbox[0],y:CUR.viewbox[1],w:CUR.viewbox[2],h:CUR.viewbox[3]};
  svg.setAttribute('viewBox',`${VB.x} ${VB.y} ${VB.w} ${VB.h}`); svg.setAttribute('width',VB.w); svg.setAttribute('height',VB.h);
  const defs=document.createElementNS(NS,'defs'); svg.appendChild(defs);
  // edges
  CUR.edges.forEach(([x1,y1,x2,y2])=>{
    const a=nearest(x1,y1), b=nearest(x2,y2); if(!a||!b||a===b) return;
    const l=document.createElementNS(NS,'line');
    l.setAttribute('x1',a.x);l.setAttribute('y1',a.y);l.setAttribute('x2',b.x);l.setAttribute('y2',b.y);
    l.setAttribute('class','edge'); svg.appendChild(l);
    edgeEls.push({el:l,a:a.s,b:b.s}); ADJ[a.s].add(b.s); ADJ[b.s].add(a.s);
  });
  // nodes
  CUR.nodes.forEach(n=>{
    const g=document.createElementNS(NS,'g'); g.setAttribute('class','node');
    const r=radius(n.cat), col=(CAT[n.cat]||CAT.passive).c;
    const dia=q=>`${n.x},${n.y-q} ${n.x+q},${n.y} ${n.x},${n.y+q} ${n.x-q},${n.y}`;
    let ring;
    if(n.shape==='s'){ring=document.createElementNS(NS,'rect');ring.setAttribute('x',n.x-r);ring.setAttribute('y',n.y-r);ring.setAttribute('width',r*2);ring.setAttribute('height',r*2);ring.setAttribute('rx',6);}
    else if(n.shape==='d'){ring=document.createElementNS(NS,'polygon');ring.setAttribute('points',dia(r));}
    else{ring=document.createElementNS(NS,'circle');ring.setAttribute('cx',n.x);ring.setAttribute('cy',n.y);ring.setAttribute('r',r);}
    ring.setAttribute('class','ring'); ring.setAttribute('stroke',col); g.appendChild(ring);
    const src=ICONS[n.s];
    if(src){
      const cid='c_'+n.s.replace(/[^a-z0-9]/gi,'_');
      const cp=document.createElementNS(NS,'clipPath'); cp.setAttribute('id',cid);
      let shp;
      if(n.shape==='s'){shp=document.createElementNS(NS,'rect');shp.setAttribute('x',n.x-r+2);shp.setAttribute('y',n.y-r+2);shp.setAttribute('width',(r-2)*2);shp.setAttribute('height',(r-2)*2);shp.setAttribute('rx',5);}
      else if(n.shape==='d'){shp=document.createElementNS(NS,'polygon');shp.setAttribute('points',dia(r-2));}
      else{shp=document.createElementNS(NS,'circle');shp.setAttribute('cx',n.x);shp.setAttribute('cy',n.y);shp.setAttribute('r',r-2);}
      cp.appendChild(shp); defs.appendChild(cp);
      const im=document.createElementNS(NS,'image'); im.setAttribute('href',src);
      im.setAttribute('x',n.x-r+2);im.setAttribute('y',n.y-r+2);im.setAttribute('width',(r-2)*2);im.setAttribute('height',(r-2)*2);
      im.setAttribute('preserveAspectRatio','xMidYMid slice'); im.setAttribute('clip-path','url(#'+cid+')'); im.setAttribute('class','art'); im.style.pointerEvents='none';
      g.appendChild(im);
    }
    if(n.cat!=='stat'){
      const words=(n.n||'').split(' '); const lines=[]; let cur='';
      words.forEach(w=>{ if((cur+' '+w).trim().length>14){lines.push(cur.trim());cur=w;} else cur+=' '+w; }); if(cur.trim())lines.push(cur.trim());
      const t=document.createElementNS(NS,'text'); t.setAttribute('x',n.x); t.setAttribute('y',n.y+r+13); t.setAttribute('font-size',n.cat==='keystone'?'15':'12');
      lines.slice(0,3).forEach((ln,i)=>{const ts=document.createElementNS(NS,'tspan');ts.setAttribute('x',n.x);ts.setAttribute('dy',i?13:0);ts.textContent=ln;t.appendChild(ts);});
      g.appendChild(t);
    }
    g.addEventListener('mouseenter',()=>show(n,g));
    g.addEventListener('click',(e)=>{e.stopPropagation(); show(n,g); toggle(n.s);});
    svg.appendChild(g); nodeEls[n.s]=g;
  });
  ROOT=(CUR.nodes.find(n=>n.cat==='root')||CUR.nodes.slice().sort((a,b)=>a.y-b.y)[0]).s;
  computeGroups();
  active=new Set([ROOT]);
  redraw(); fit();
}
// Mutually-exclusive groups: cluster each exclusive category by row (y) so classes
// with more than one "pick-one" group (e.g. Arbites keystones + Cyber-Mastiff) work.
function computeGroups(){
  for(const cat of Object.keys(EXCL)){
    const ns=CUR.nodes.filter(n=>n.cat===cat).sort((a,b)=>a.y-b.y);
    let gi=0,last=-9999;
    ns.forEach(n=>{ if(n.y-last>80) gi++; last=n.y; n._grp=cat+'#'+gi; });
  }
}

function isAvail(slug){ if(active.has(slug))return false; for(const a of active){if(ADJ[slug].has(a))return true;} return false; }
function points(){ return active.size-1; }
function exclConflict(slug){ const nd=nodeBySlug[slug]; if(!EXCL[nd.cat])return null; for(const a of active){ const an=nodeBySlug[a]; if(a!==slug&&an&&an._grp&&an._grp===nd._grp) return an.n; } return null; }
function toggle(slug){ if(slug===ROOT)return; if(active.has(slug))deselect(slug); else select(slug); }
function select(slug){
  const n=nodeBySlug[slug], conflict=exclConflict(slug);
  if(conflict){ toast(`Only one ${EXCL[n.cat]} allowed — remove "${conflict}" first.`); return; }
  if(PMAX!=null && points()>=PMAX){ toast(`No points left (${PMAX}/${PMAX}). Remove a node first.`); return; }
  if(!isAvail(slug)){ toast('Not connected — allocate a linked node first.'); return; }
  active.add(slug); redraw();
}
function deselect(slug){
  const trial=new Set(active); trial.delete(slug);
  const seen=new Set([ROOT]), q=[ROOT];
  while(q.length){const cur=q.pop(); for(const nb of ADJ[cur]){ if(trial.has(nb)&&!seen.has(nb)){seen.add(nb);q.push(nb);} }}
  if([...trial].some(a=>a!==ROOT&&!seen.has(a))){ toast('Can\u2019t remove \u2014 other nodes connect through it. Remove those first.'); return; }
  active.delete(slug); redraw();
}
function show(n,g){
  document.querySelectorAll('.node.hot').forEach(e=>e.classList.remove('hot')); if(g)g.classList.add('hot');
  const st=active.has(n.s)?'<span style="color:var(--glow)">\u25cf Allocated</span>':isAvail(n.s)?'<span style="color:var(--muted)">Available \u2014 click to allocate</span>':'<span style="color:var(--muted)">Locked \u2014 connect a path first</span>';
  info.innerHTML=`<div class="type">${n.t||CAT[n.cat].label} \u00b7 ${CAT[n.cat].label}</div><h2>${n.n||'Class node'}</h2><p>${n.d||''}</p><p class="hint" style="margin-top:12px">${st}</p>`;
}
function pick(cat){ return CUR.nodes.filter(n=>active.has(n.s)&&n.cat===cat).map(n=>n.n); }
function redraw(){
  CUR.nodes.forEach(n=>{const g=nodeEls[n.s]; g.classList.remove('active','avail','locked');
    if(active.has(n.s))g.classList.add('active'); else if(isAvail(n.s))g.classList.add('avail'); else g.classList.add('locked');});
  edgeEls.forEach(e=>{const on=active.has(e.a)&&active.has(e.b); e.el.classList.toggle('on',on); e.el.style.opacity=on?1:.28;});
  const p=points(), cap=(PMAX!=null?`${p} / ${PMAX}`:`${p}`);
  ptsN.textContent=cap; ptsN.classList.toggle('full',PMAX!=null&&p>=PMAX);
  document.getElementById('ptsL').textContent=(PMAX!=null?'Points spent':'Perks chosen');
  const ks=pick('keystone').join(', ')||'\u2014',ab=pick('ability').join(', ')||'\u2014',bl=pick('blitz')[0]||'\u2014',au=pick('aura')[0]||'\u2014',md=pick('keymod').length+pick('abilmod').length;
  sumEl.innerHTML=`<h3>${CUR.name} \u2014 build summary</h3>
    <div class="chip"><span class="k">${PMAX!=null?'Points spent':'Perks chosen'}</span><span class="pts">${cap}</span></div>
    <div class="chip"><span class="k">Keystone</span><b style="color:var(--gold)">${ks}</b></div>
    <div class="chip"><span class="k">Ability</span><b style="color:var(--ability)">${ab}</b></div>
    <div class="chip"><span class="k">Blitz</span><b style="color:var(--blitz)">${bl}</b></div>
    <div class="chip"><span class="k">Aura</span><b style="color:var(--aura)">${au}</b></div>
    <div class="chip"><span class="k">Modifiers</span><b>${md}</b></div>`;
}
let toastT; function toast(m){toastEl.textContent=m;toastEl.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>toastEl.classList.remove('show'),2600);}

/* class switcher */
const cbar=document.getElementById('classbar');
DATA.classes.forEach(c=>{const b=document.createElement('button');b.textContent=c.name;b.dataset.key=c.key;
  b.onclick=()=>{cbar.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');buildClass(c.key);};cbar.appendChild(b);});
document.getElementById('resetBtn').onclick=()=>{active=new Set([ROOT]);redraw();};

/* legend */
const legend=document.getElementById('legend');
Object.values(CAT).forEach(c=>{const s=document.createElement('span');s.innerHTML=`<i style="background:${c.c}"></i>${c.label}`;legend.appendChild(s);});

/* version / provenance footer */
document.getElementById('ver').innerHTML=`Skill Tree Editor <b>v${APP_VERSION}</b> &nbsp;·&nbsp; Tree data based on <b>${GAME_PATCH}</b><br>Data via ${DATA_SOURCE}, scraped ${DATA_SCRAPED}. Community source — wording may lag a patch.`;

/* PNG export */
const EXPORT_CSS=`.edge{stroke:#2c3037;stroke-width:3}.edge.on{stroke:#4fc9d4;stroke-width:5}.ring{fill:#16181c;stroke-width:3}
text{font-family:Georgia,serif;fill:#d7dade;text-anchor:middle;paint-order:stroke;stroke:#000;stroke-width:3px;stroke-linejoin:round}
.node.locked{opacity:.16}.node.locked .art{filter:grayscale(1)}.node.avail{opacity:.7}.node.active .ring{stroke-width:5}`;
function exportPNG(){
  const w=VB.w,h=VB.h,headH=104,sc=2;
  const clone=svg.cloneNode(true); clone.setAttribute('xmlns',NS); clone.removeAttribute('style');
  clone.setAttribute('viewBox',`${VB.x} ${VB.y} ${w} ${h}`); clone.setAttribute('width',w); clone.setAttribute('height',h);
  const st=document.createElementNS(NS,'style'); st.textContent=EXPORT_CSS; clone.insertBefore(st,clone.firstChild);
  const bg=document.createElementNS(NS,'rect'); bg.setAttribute('x',VB.x);bg.setAttribute('y',VB.y);bg.setAttribute('width',w);bg.setAttribute('height',h);bg.setAttribute('fill','#0c0d0f');
  clone.insertBefore(bg,st.nextSibling);
  const str=new XMLSerializer().serializeToString(clone), img=new Image();
  img.onload=()=>{try{
    const cv=document.createElement('canvas'); cv.width=w*sc; cv.height=(h+headH)*sc; const cx=cv.getContext('2d');
    cx.fillStyle='#0c0d0f'; cx.fillRect(0,0,cv.width,cv.height);
    const name=(document.getElementById('buildName').value||'Build').trim();
    cx.fillStyle='#8b9099'; cx.font=`${15*sc}px system-ui,sans-serif`; cx.fillText('WARHAMMER 40,000: DARKTIDE \u00b7 '+CUR.name.toUpperCase(), 30*sc, 22*sc);
    cx.fillStyle='#e0b23c'; cx.font=`600 ${30*sc}px Georgia,serif`; cx.fillText(name, 30*sc, 44*sc);
    const ks=pick('keystone')[0]||'\u2014',ab=pick('ability')[0]||'\u2014',bl=pick('blitz')[0]||'\u2014',au=pick('aura')[0]||'\u2014';
    cx.fillStyle='#c3c7cd'; cx.font=`${15*sc}px system-ui,sans-serif`;
    const hdr=(PMAX!=null?`${points()}/${PMAX} pts   \u00b7   Keystone: ${ks}   \u00b7   Ability: ${ab}   \u00b7   Blitz: ${bl}   \u00b7   Aura: ${au}`:`${points()} Stimm perks chosen`);
    cx.fillText(hdr, 30*sc, 78*sc);
    cx.textAlign='right'; cx.fillStyle='#5c626b'; cx.font=`${13*sc}px system-ui,sans-serif`;
    cx.fillText(`Editor v${APP_VERSION}`, cv.width-30*sc, 30*sc);
    cx.fillText(GAME_PATCH+' · via '+DATA_SOURCE, cv.width-30*sc, 50*sc);
    cx.textAlign='left';
    cx.strokeStyle='#262a31'; cx.lineWidth=sc; cx.beginPath(); cx.moveTo(0,(headH-1)*sc); cx.lineTo(cv.width,(headH-1)*sc); cx.stroke();
    cx.drawImage(img,0,headH*sc,w*sc,h*sc);
    cv.toBlob(b=>{const a=document.createElement('a');a.download=(CUR.name+'_'+name).replace(/[^a-z0-9]+/gi,'_')+'.png';a.href=URL.createObjectURL(b);a.click();setTimeout(()=>URL.revokeObjectURL(a.href),4000);},'image/png');
  }catch(err){toast('Export failed: '+err.message);}};
  img.onerror=()=>toast('Export failed to render.');
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(str);
}
document.getElementById('exportBtn').onclick=exportPNG;

/* pan + zoom */
const stage=document.getElementById('stage'); let scale=1,tx=0,ty=0;
function ap(){svg.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;}
function fit(){const r=stage.getBoundingClientRect();const s=Math.min(r.width/VB.w,r.height/VB.h)*0.95;scale=s;tx=(r.width-VB.w*s)/2;ty=(r.height-VB.h*s)/2+4;ap();}
document.getElementById('zin').onclick=()=>{scale*=1.2;ap();};
document.getElementById('zout').onclick=()=>{scale/=1.2;ap();};
document.getElementById('zfit').onclick=fit;
let drag=false,sx,sy;
stage.addEventListener('mousedown',e=>{if(e.target.closest('.node'))return;drag=true;sx=e.clientX-tx;sy=e.clientY-ty;stage.classList.add('grab');});
addEventListener('mousemove',e=>{if(drag){tx=e.clientX-sx;ty=e.clientY-sy;ap();}});
addEventListener('mouseup',()=>{drag=false;stage.classList.remove('grab');});
stage.addEventListener('wheel',e=>{e.preventDefault();const r=stage.getBoundingClientRect();const mx=e.clientX-r.left,my=e.clientY-r.top;const f=e.deltaY<0?1.12:1/1.12;tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;ap();},{passive:false});

/* boot */
cbar.querySelector('button').classList.add('on');
buildClass(DATA.classes[0].key);
</script>
"""

html = TEMPLATE.replace('__DATA__', data)
open(r'C:/AI Bins/Code/Darktide/darktide-skill-trees.html','w',encoding='utf-8').write(html)
import os
print('WROTE html MB:', round(os.path.getsize(r'C:/AI Bins/Code/Darktide/darktide-skill-trees.html')/1e6,2))
