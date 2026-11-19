import uuid

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Basic Continuous-Time Signals",
    layout="wide",
)

# Remove Streamlit's default padding/header so the app fills the page
st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    header[data-testid="stHeader"] {height: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

uid = "sigview_" + uuid.uuid4().hex[:8]

html = r"""
<div id="ROOT_ID" class="animation-app">

<style>
#ROOT_ID {
    width:100%;
    max-width:1500px;
    margin:auto;
    padding:clamp(8px, 2vw, 24px);
    box-sizing:border-box;
    font-family:Arial,sans-serif;
    position:relative;
    color:#1f2a44;
    background:linear-gradient(160deg,#f7f9ff 0%,#eaf0fc 100%);
    border-radius:18px;
    box-shadow:0 10px 30px rgba(31,42,68,0.10);
}

#ROOT_ID * { box-sizing:border-box; }

#ROOT_ID h2 {
    text-align:center;
    font-size:clamp(20px, 2.6vw, 30px);
    margin:12px 0 4px;
    letter-spacing:0.5px;
    background:linear-gradient(90deg,#2f6fed,#12a36a);
    -webkit-background-clip:text;
    background-clip:text;
    -webkit-text-fill-color:transparent;
    color:transparent;
}

#ROOT_ID .subtitle {
    text-align:center;
    font-size:clamp(13px,1.6vw,17px);
    margin:0 0 18px;
    opacity:0.8;
}

#ROOT_ID button.theme {
    color:white;
    border:0;
    border-radius:10px;
    cursor:pointer;
    font-weight:bold;
    white-space:nowrap;
    touch-action:manipulation;
    box-shadow:0 4px 10px rgba(0,0,0,0.22);
    transition:transform .12s, filter .12s;
    background:linear-gradient(135deg,#8b6cff,#5a3fd4);
    position:absolute;
    top:clamp(24px,3vw,36px);
    right:clamp(8px,1.5vw,16px);
    padding:8px 14px;
    font-size:clamp(12px,1.3vw,14px);
    z-index:2;
}
#ROOT_ID button.theme:hover { transform:translateY(-1px); filter:brightness(1.08); }
#ROOT_ID button.theme:active { transform:scale(0.97); }

/* ---------- two-column layout ---------- */
#ROOT_ID .layout {
    display:grid;
    grid-template-columns:310px minmax(0,1fr);
    gap:18px;
    align-items:start;
}

#ROOT_ID .panel {
    background:linear-gradient(180deg,#ffffff,#f0f4fc);
    border:1px solid #cdd7ec;
    border-radius:14px;
    box-shadow:0 6px 18px rgba(31,42,68,0.12);
    padding:14px;
}

#ROOT_ID .left { display:flex; flex-direction:column; gap:14px; }

#ROOT_ID .panel h3 { margin:0 0 10px; font-size:17px; }
#ROOT_ID .sigcard { --c:#2f6fed; }
#ROOT_ID .sigcard h3 { color:var(--c); }

#ROOT_ID .tiles {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
}

#ROOT_ID .tile {
    cursor:pointer;
    border:2px solid #d3dcf0;
    border-radius:10px;
    padding:6px 4px 5px;
    text-align:center;
    font-size:12px;
    font-weight:bold;
    background:#ffffff;
    user-select:none;
    transition:border-color .12s, box-shadow .12s;
}
#ROOT_ID .tile:hover { border-color:var(--c); }
#ROOT_ID .tile.active {
    border-color:var(--c);
    box-shadow:0 0 0 3px color-mix(in srgb, var(--c) 25%, transparent);
}
#ROOT_ID .tile svg { display:block; width:100%; height:36px; stroke:var(--c); fill:none; }

#ROOT_ID .formula {
    margin:12px 0 0;
    padding:8px 10px;
    border-radius:8px;
    background:rgba(47,111,237,0.08);
    font-size:14px;
    font-weight:bold;
    text-align:center;
}

#ROOT_ID .desc {
    display:none;
    margin-top:10px;
    font-size:13px;
    line-height:1.5;
    opacity:0.85;
}
#ROOT_ID .desc.show { display:block; }

#ROOT_ID .param {
    display:none;
    margin-top:10px;
    font-size:13px;
    font-weight:bold;
}
#ROOT_ID .param.show { display:block; }

#ROOT_ID input[type=number] {
    display:block;
    width:100%;
    margin-top:5px;
    padding:7px;
    font-size:15px;
    border:1px solid #b9c5e0;
    border-radius:8px;
    background:#ffffff;
    color:#1f2a44;
    text-align:center;
}
#ROOT_ID input[type=number]:focus {
    outline:none;
    border-color:#2f6fed;
    box-shadow:0 0 0 3px rgba(47,111,237,0.25);
}
#ROOT_ID input[type=number]:disabled { opacity:0.55; cursor:not-allowed; }

#ROOT_ID .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
#ROOT_ID .grid2 label { font-size:13px; font-weight:bold; }

#ROOT_ID .subhead {
    margin:14px 0 6px;
    font-size:14px;
    font-weight:bold;
}

#ROOT_ID .seg {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:6px;
    margin-bottom:10px;
}
#ROOT_ID .seg div {
    cursor:pointer;
    text-align:center;
    padding:7px 4px;
    border:2px solid #d3dcf0;
    border-radius:9px;
    background:#ffffff;
    font-size:13px;
    font-weight:bold;
    user-select:none;
}
#ROOT_ID .seg div.active {
    border-color:#2f6fed;
    box-shadow:0 0 0 3px rgba(47,111,237,0.22);
    color:#2f6fed;
}

#ROOT_ID .hint { margin-top:8px; font-size:12px; opacity:0.75; line-height:1.45; }

/* ---------- right column ---------- */
#ROOT_ID .right { min-width:0; }

#ROOT_ID .status {
    text-align:center;
    width:fit-content;
    max-width:100%;
    margin:0 auto 12px;
    padding:9px 20px;
    border-radius:999px;
    background:#ffffff;
    border:1px solid #d3dcf0;
    box-shadow:0 3px 10px rgba(31,42,68,0.08);
    font-size:clamp(12px,1.5vw,16px);
    font-weight:bold;
}

#ROOT_ID canvas {
    display:block;
    max-width:100%;
    background:linear-gradient(180deg,#ffffff,#f0f4fc);
    border:1px solid #cdd7ec;
    border-radius:14px;
    box-shadow:0 6px 18px rgba(31,42,68,0.12);
}

/* ---------- dark mode ---------- */
#ROOT_ID.dark {
    background:linear-gradient(160deg,#0d1117 0%,#161d2e 100%);
    color:#e6edf7;
    box-shadow:0 10px 30px rgba(0,0,0,0.45);
}
#ROOT_ID.dark h2 {
    background:linear-gradient(90deg,#6aa9ff,#3ddc97);
    -webkit-background-clip:text;
    background-clip:text;
    -webkit-text-fill-color:transparent;
}
#ROOT_ID.dark .panel,
#ROOT_ID.dark canvas {
    background:linear-gradient(180deg,#1b2336,#111724);
    border-color:#2f3b57;
    box-shadow:0 6px 18px rgba(0,0,0,0.5);
}
#ROOT_ID.dark .sigcard { --c:#58a6ff; }
#ROOT_ID.dark .tile,
#ROOT_ID.dark .seg div { background:#0f1522; border-color:#33415f; }
#ROOT_ID.dark .tile:hover,
#ROOT_ID.dark .tile.active { border-color:var(--c); }
#ROOT_ID.dark .seg div.active { border-color:#58a6ff; color:#6aa9ff; box-shadow:0 0 0 3px rgba(88,166,255,0.28); }
#ROOT_ID.dark .formula { background:rgba(88,166,255,0.12); }
#ROOT_ID.dark input[type=number] {
    background:#0f1522;
    color:#e6edf7;
    border-color:#3b4866;
}
#ROOT_ID.dark input[type=number]:focus {
    border-color:#58a6ff;
    box-shadow:0 0 0 3px rgba(88,166,255,0.30);
}
#ROOT_ID.dark .status {
    background:#1a2233;
    border-color:#33415f;
    color:#e6edf7;
    box-shadow:0 3px 12px rgba(0,0,0,0.4);
}

/* ---------- responsive ---------- */
@media (max-width:900px) {
    #ROOT_ID .layout { grid-template-columns:1fr; }
    #ROOT_ID .left { flex-direction:row; flex-wrap:wrap; }
    #ROOT_ID .left .panel { flex:1 1 280px; }
}

@media (max-width:550px) {
    #ROOT_ID { padding:6px; }
    #ROOT_ID h2 { margin-top:64px; }
    #ROOT_ID button.theme { padding:7px 11px; }
}
</style>

<button class="theme" id="theme">🌙 DARK MODE</button>

<h2>Basic Continuous-Time Signals</h2>
<div class="subtitle">Choose a signal, set its parameters and the plotting area</div>

<div class="layout">

    <!-- LEFT COLUMN -->
    <div class="left">

        <div class="panel sigcard" id="card_sig"></div>

        <div class="panel" id="card_axes">
            <h3>Plotting area</h3>

            <div class="subhead" style="margin-top:0">Time axis</div>
            <div class="grid2">
                <label>t<sub>min</sub> (s)
                    <input id="tmin" type="number" value="-10" min="-1000" max="999" step="1">
                </label>
                <label>t<sub>max</sub> (s)
                    <input id="tmax" type="number" value="10" min="-999" max="1000" step="1">
                </label>
            </div>

            <div class="subhead">Amplitude axis</div>
            <div class="seg">
                <div id="m_auto" class="active">Auto scale</div>
                <div id="m_fixed">Fixed values</div>
            </div>

            <div class="grid2">
                <label>Min amplitude
                    <input id="ymin" type="number" value="-1" step="0.5" disabled>
                </label>
                <label>Max amplitude
                    <input id="ymax" type="number" value="1" step="0.5" disabled>
                </label>
            </div>

            <div class="hint" id="axhint">Auto scale fits the amplitude axis to the signal. The boxes show the range currently used.</div>
        </div>

    </div>

    <!-- RIGHT COLUMN -->
    <div class="right">
        <div class="status" id="status"></div>
        <canvas id="cv"></canvas>
    </div>

</div>

<script>
(function(){

const root=document.getElementById("ROOT_ID");
const $=s=>root.querySelector(s);

// ======================================
// SIGNAL DEFINITIONS
// ======================================

const TYPES={
    exp:  {label:"Real exponential",
           path:"M2 24 C18 23 28 20 36 4"},
    sine: {label:"Sinusoidal",
           path:"M2 14 C7 0 13 0 19 14 S31 28 38 14"},
    step: {label:"Unit step",
           path:"M2 24 H19 V6 H38"},
    imp:  {label:"Unit impulse",
           path:"M2 24 H38 M20 24 V6 M15.5 11 L20 5 L24.5 11"}
};

const ORDER=["exp","sine","step","imp"];

const PARAMS=[
    {p:"C",label:"Amplitude C",         types:["exp"],  min:-100, max:100, step:0.1},
    {p:"a",label:"Rate a (real)",       types:["exp"],  min:-10,  max:10,  step:0.1},
    {p:"A",label:"Amplitude A",         types:["sine"], min:-100, max:100, step:0.1},
    {p:"f",label:"Frequency f (Hz)",    types:["sine"], min:0,     max:20,  step:0.1},
    {p:"phi",label:"Phase φ (radians)",   types:["sine"], min:-100,  max:100, step:0.1}
];

const DESCS={
    step:"u(t) = 1 for t ≥ 0 and 0 for t &lt; 0.",
    imp:"δ(t) has unit area concentrated at t = 0. It is drawn as an arrow of height 1."
};

const sig={type:"exp", C:1, a:0.5, A:1, f:1, phi:0};

const view={tmin:-10, tmax:10, auto:true, ymin:-1, ymax:1};

// ======================================
// LEFT COLUMN: SIGNAL CARD
// ======================================

function buildCard(){

    const card=$("#card_sig");

    let h='<h3>Signal type</h3><div class="tiles">';

    ORDER.forEach(id=>{
        h+='<div class="tile" data-type="'+id+'">'+
           '<svg viewBox="0 0 40 28"><path d="'+TYPES[id].path+
           '" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'+
           TYPES[id].label+'</div>';
    });

    h+='</div><div class="formula" id="formula"></div>';

    PARAMS.forEach(q=>{
        h+='<label class="param" data-for="'+q.types.join(" ")+'">'+q.label+
           '<input type="number" data-p="'+q.p+'" min="'+q.min+'" max="'+q.max+
           '" step="'+q.step+'" value="'+sig[q.p]+'"></label>';
    });

    Object.keys(DESCS).forEach(id=>{
        h+='<div class="desc" data-for="'+id+'">'+DESCS[id]+'</div>';
    });

    card.innerHTML=h;

    card.querySelectorAll(".tile").forEach(el=>{
        el.addEventListener("click",()=>{
            sig.type=el.dataset.type;
            refreshCard();
            render();
        });
    });

    card.querySelectorAll(".param input").forEach(inp=>{
        inp.addEventListener("change",()=>{

            const p=inp.dataset.p;
            let v=Number(inp.value);

            const lo=Number(inp.min), hi=Number(inp.max);
            if(!Number.isFinite(v)) v=sig[p];
            v=Math.min(hi,Math.max(lo,v));

            inp.value=v;
            sig[p]=v;
            render();
        });
    });

    refreshCard();
}

function refreshCard(){

    const card=$("#card_sig");

    card.querySelectorAll(".tile").forEach(el=>{
        el.classList.toggle("active",el.dataset.type===sig.type);
    });

    card.querySelectorAll(".param, .desc").forEach(el=>{
        el.classList.toggle("show",el.dataset.for.split(" ").includes(sig.type));
    });
}

buildCard();

// ======================================
// PLOT AREA SETTINGS (left column)
// ======================================

const tminIn=$("#tmin"), tmaxIn=$("#tmax"), yminIn=$("#ymin"), ymaxIn=$("#ymax");

function applyTime(){

    const a=Number(tminIn.value), b=Number(tmaxIn.value);

    if(!Number.isFinite(a)||!Number.isFinite(b)||b<=a){
        tminIn.value=view.tmin;
        tmaxIn.value=view.tmax;
        return;
    }

    view.tmin=a;
    view.tmax=b;
    render();
}

function applyY(){

    const a=Number(yminIn.value), b=Number(ymaxIn.value);

    if(!Number.isFinite(a)||!Number.isFinite(b)||b<=a){
        yminIn.value=view.ymin;
        ymaxIn.value=view.ymax;
        return;
    }

    view.ymin=a;
    view.ymax=b;
    render();
}

tminIn.addEventListener("change",applyTime);
tmaxIn.addEventListener("change",applyTime);
yminIn.addEventListener("change",applyY);
ymaxIn.addEventListener("change",applyY);

function setMode(auto){

    view.auto=auto;

    $("#m_auto").classList.toggle("active",auto);
    $("#m_fixed").classList.toggle("active",!auto);

    yminIn.disabled=auto;
    ymaxIn.disabled=auto;

    $("#axhint").textContent=auto
        ? "Auto scale fits the amplitude axis to the signal. The boxes show the range currently used."
        : "Fixed values: the amplitude axis uses exactly the minimum and maximum above.";

    render();
}

$("#m_auto").addEventListener("click",()=>setMode(true));
$("#m_fixed").addEventListener("click",()=>setMode(false));

// ======================================
// THEMES
// ======================================

const themes={
    light:{text:"#1f2a44",tick:"#44506e",axis:"#44506e",zero:"#9aa6bf",grid:"#e0e6f3",
           line:"#2f6fed",accent:"#e5484d",ring:"#ffffff",
           legendBg:"rgba(255,255,255,0.92)",glow:5},
    dark:{text:"#e6edf7",tick:"#b4c0d9",axis:"#b4c0d9",zero:"#6e7b96",grid:"#27324a",
          line:"#58a6ff",accent:"#ff6b6b",ring:"#111724",
          legendBg:"rgba(15,21,34,0.92)",glow:14}
};

let darkMode=!!(window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches);
let C=themes.light;
const themeBtn=$("#theme");

function applyTheme(){
    C=darkMode?themes.dark:themes.light;
    root.classList.toggle("dark",darkMode);
    themeBtn.textContent=darkMode?"☀ LIGHT MODE":"🌙 DARK MODE";
}

themeBtn.addEventListener("click",()=>{
    darkMode=!darkMode;
    applyTheme();
    render();
});

applyTheme();

// ======================================
// MATH HELPERS
// ======================================

function num(v){
    // short readable number for formulas
    const r=Math.round(v*1e4)/1e4;
    return String(r);
}

function valueAt(t){
    if(sig.type==="exp")  return sig.C*Math.exp(sig.a*t);
    if(sig.type==="sine") return sig.A*Math.cos(2*Math.PI*sig.f*t+sig.phi);
    if(sig.type==="step") return t>=0?1:0;
    return 0;
}

function equation(){
    if(sig.type==="exp")
        return "x(t) = "+num(sig.C)+" · exp("+num(sig.a)+" t)";
    if(sig.type==="sine")
        return "x(t) = "+num(sig.A)+" · cos(2π · "+num(sig.f)+" · t"+
               (sig.phi<0?" − "+num(-sig.phi):" + "+num(sig.phi))+")";
    if(sig.type==="step") return "x(t) = u(t)";
    return "x(t) = δ(t)";
}

function padRange(lo,hi){

    lo=Math.min(0,lo);
    hi=Math.max(0,hi);

    let span=hi-lo;
    if(span<1e-12){ lo=-1; hi=1; span=2; }

    return [lo-0.12*span, hi+0.12*span];
}

// sampled curve for exponentials and sinusoids
function sampleCurve(){

    const span=view.tmax-view.tmin;
    let n=2000;

    if(sig.type==="sine") n=Math.min(40000,Math.max(2000,Math.ceil(span*sig.f*40)));

    const ts=new Float64Array(n+1), vs=new Float64Array(n+1);

    for(let i=0;i<=n;i++){
        const t=view.tmin+span*i/n;
        ts[i]=t;
        const v=valueAt(t);
        // values beyond 1e15 are not drawn (they would overflow the axis)
        vs[i]=(Number.isFinite(v)&&Math.abs(v)<=1e15)?v:NaN;
    }

    return {ts,vs,n};
}

function autoRange(curve){

    if(sig.type==="step") return padRange(0,1);
    if(sig.type==="imp")  return padRange(0,1);

    let lo=0, hi=0;

    for(let i=0;i<=curve.n;i++){
        const v=curve.vs[i];
        if(Number.isNaN(v)) continue;
        if(v<lo) lo=v;
        if(v>hi) hi=v;
    }

    return padRange(lo,hi);
}

// ======================================
// CANVAS
// ======================================

const cv=$("#cv");
const dpr=()=>window.devicePixelRatio||1;
let hoverX=null;

function fit(){

    const w=Math.max(280,Math.floor(cv.parentElement.clientWidth));
    const h=Math.round(Math.min(600,Math.max(340,w*0.56)));

    cv._w=w;
    cv._h=h;
    cv.style.width=w+"px";
    cv.style.height=h+"px";
    cv.width=Math.round(w*dpr());
    cv.height=Math.round(h*dpr());
}

function niceTicks(a,b,n){

    const raw=(b-a)/n;
    const mag=Math.pow(10,Math.floor(Math.log10(raw)));
    const r=raw/mag;
    const step=(r<=1?1:r<=2?2:r<=5?5:10)*mag;

    const ticks=[];
    for(let v=Math.ceil(a/step-1e-9)*step; v<=b+1e-9; v+=step){
        ticks.push(Math.abs(v)<step*1e-9?0:v);
    }

    return {ticks,step};
}

function fmt(v,step){

    if(v===0) return "0";

    if(Math.abs(v)>=1e5 || Math.abs(v)<1e-3)
        return v.toExponential(1).replace("e+","e");

    const dec=Math.max(0,-Math.floor(Math.log10(step)+1e-9));
    return v.toFixed(Math.min(dec,6));
}

function roundRect(ctx,x,y,w,h,r){
    ctx.beginPath();
    ctx.moveTo(x+r,y);
    ctx.arcTo(x+w,y,x+w,y+h,r);
    ctx.arcTo(x+w,y+h,x,y+h,r);
    ctx.arcTo(x,y+h,x,y,r);
    ctx.arcTo(x,y,x+w,y,r);
    ctx.closePath();
}

function render(){

    const W=cv._w, H=cv._h;
    const ctx=cv.getContext("2d");

    ctx.setTransform(dpr(),0,0,dpr(),0,0);
    ctx.clearRect(0,0,W,H);
    ctx.lineJoin="round";

    $("#formula").textContent=equation();

    // ----- amplitude range
    const curve=(sig.type==="exp"||sig.type==="sine")?sampleCurve():null;

    let ymin, ymax;

    if(view.auto){

        [ymin,ymax]=autoRange(curve);

        const dec=3;
        view.ymin=Number(ymin.toFixed(dec));
        view.ymax=Number(ymax.toFixed(dec));
        yminIn.value=view.ymin;
        ymaxIn.value=view.ymax;
    }
    else{
        ymin=view.ymin;
        ymax=view.ymax;
    }

    $("#status").textContent=
        equation()+"     |     t: "+num(view.tmin)+" … "+num(view.tmax)+" s"+
        "     |     amplitude: "+num(ymin)+" … "+num(ymax)+(view.auto?" (auto)":" (fixed)");

    // ----- plot geometry
    const L=68, R=W-24, T=40, B=H-48;

    const X=t=>L+(t-view.tmin)/(view.tmax-view.tmin)*(R-L);
    const Y=v=>B-(v-ymin)/(ymax-ymin)*(B-T);

    // ----- grid and tick labels
    const xt=niceTicks(view.tmin,view.tmax,Math.max(4,Math.floor((R-L)/90)));
    const yt=niceTicks(ymin,ymax,Math.max(4,Math.floor((B-T)/55)));

    ctx.font="12px Arial";
    ctx.lineWidth=1;

    xt.ticks.forEach(v=>{
        const x=X(v);

        ctx.strokeStyle=C.grid;
        ctx.beginPath(); ctx.moveTo(x,T); ctx.lineTo(x,B); ctx.stroke();

        ctx.fillStyle=C.tick;
        ctx.textAlign="center";
        ctx.fillText(fmt(v,xt.step),x,B+18);
    });

    yt.ticks.forEach(v=>{
        const y=Y(v);

        ctx.strokeStyle=C.grid;
        ctx.beginPath(); ctx.moveTo(L,y); ctx.lineTo(R,y); ctx.stroke();

        ctx.fillStyle=C.tick;
        ctx.textAlign="right";
        ctx.fillText(fmt(v,yt.step),L-8,y+4);
    });

    // zero lines (only when visible)
    ctx.strokeStyle=C.zero;
    ctx.lineWidth=1.6;
    ctx.beginPath();
    if(ymin<=0&&ymax>=0){ ctx.moveTo(L,Y(0)); ctx.lineTo(R,Y(0)); }
    if(view.tmin<=0&&view.tmax>=0){ ctx.moveTo(X(0),T); ctx.lineTo(X(0),B); }
    ctx.stroke();

    // frame
    ctx.strokeStyle=C.axis;
    ctx.lineWidth=1.5;
    ctx.beginPath();
    ctx.moveTo(L,T); ctx.lineTo(L,B); ctx.lineTo(R,B);
    ctx.stroke();

    // titles and axis labels
    ctx.fillStyle=C.text;
    ctx.textAlign="left";
    ctx.font="bold 16px Arial";
    ctx.fillText(equation(),L,26);

    ctx.textAlign="center";
    ctx.font="14px Arial";
    ctx.fillText("t  (seconds)",(L+R)/2,H-10);

    ctx.save();
    ctx.translate(18,(T+B)/2);
    ctx.rotate(-Math.PI/2);
    ctx.fillText("x(t)",0,0);
    ctx.restore();

    // ----- signal
    ctx.save();
    ctx.beginPath();
    ctx.rect(L,T,R-L,B-T);
    ctx.clip();

    ctx.strokeStyle=C.line;
    ctx.fillStyle=C.line;
    ctx.lineWidth=3.2;
    ctx.lineCap="round";

    ctx.save();
    ctx.shadowColor=C.line;
    ctx.shadowBlur=C.glow;

    if(sig.type==="exp"||sig.type==="sine"){

        ctx.beginPath();
        let pen=false;

        for(let i=0;i<=curve.n;i++){

            const v=curve.vs[i];

            if(Number.isNaN(v)){ pen=false; continue; }

            const x=X(curve.ts[i]);
            const y=Math.max(-1e5,Math.min(1e5,Y(v)));

            if(!pen){ ctx.moveTo(x,y); pen=true; } else ctx.lineTo(x,y);
        }

        ctx.stroke();
    }
    else if(sig.type==="step"){

        const x0=Math.min(R,Math.max(L,X(0)));

        // 0 for t < 0, 1 for t >= 0
        ctx.beginPath();
        ctx.moveTo(L,Y(0)); ctx.lineTo(x0,Y(0));
        ctx.moveTo(x0,Y(1)); ctx.lineTo(R,Y(1));
        ctx.stroke();

        // vertical jump (dashed)
        if(view.tmin<=0&&view.tmax>=0){
            ctx.save();
            ctx.lineWidth=2;
            ctx.setLineDash([6,6]);
            ctx.globalAlpha=0.55;
            ctx.beginPath();
            ctx.moveTo(x0,Y(0)); ctx.lineTo(x0,Y(1));
            ctx.stroke();
            ctx.restore();

            // filled circle at (0, 1)
            ctx.beginPath(); ctx.arc(x0,Y(1),5.5,0,2*Math.PI); ctx.fill();
        }
    }
    else{

        // unit impulse: arrow of height 1 at t = 0
        if(view.tmin<=0&&view.tmax>=0){

            const x0=X(0), y0=Y(0), y1=Y(1);
            const dir=y1<y0?1:-1;       // arrow points toward the value 1

            ctx.lineWidth=4;
            ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x0,y1+dir*8); ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(x0,y1);
            ctx.lineTo(x0-8,y1+dir*18);
            ctx.lineTo(x0+8,y1+dir*18);
            ctx.closePath();
            ctx.fill();
        }
    }

    ctx.restore();   // glow

    ctx.restore();   // clip

    // label for the impulse height / out-of-range notes
    if(sig.type==="imp"){

        ctx.textAlign="left";
        ctx.font="bold 14px Arial";
        ctx.fillStyle=C.line;

        if(view.tmin<=0&&view.tmax>=0){
            const ty=Math.max(T+14,Math.min(B-6,Y(1)+4));
            ctx.fillText("(1)",X(0)+14,ty);
        }
        else{
            ctx.fillStyle=C.tick;
            ctx.fillText("δ(t) is at t = 0, which is outside the plotted time range.",L+12,T+24);
        }
    }

    // ----- hover read-out
    if(hoverX!==null && sig.type!=="imp" && hoverX>=L && hoverX<=R){

        const t=view.tmin+(hoverX-L)/(R-L)*(view.tmax-view.tmin);
        const v=valueAt(t);

        ctx.save();
        ctx.strokeStyle=C.accent;
        ctx.globalAlpha=0.7;
        ctx.lineWidth=1.5;
        ctx.setLineDash([5,5]);
        ctx.beginPath(); ctx.moveTo(hoverX,T); ctx.lineTo(hoverX,B); ctx.stroke();
        ctx.restore();

        if(Number.isFinite(v)){

            const py=Y(v);

            if(py>=T&&py<=B){
                ctx.fillStyle=C.accent;
                ctx.beginPath(); ctx.arc(hoverX,py,6,0,2*Math.PI); ctx.fill();
                ctx.strokeStyle=C.ring;
                ctx.lineWidth=2;
                ctx.beginPath(); ctx.arc(hoverX,py,6,0,2*Math.PI); ctx.stroke();
            }

            const label="t = "+t.toFixed(3)+" s,   x(t) = "+(Math.abs(v)>=1e5?v.toExponential(3):v.toFixed(3));

            ctx.font="bold 13px Arial";
            const w=ctx.measureText(label).width+20;
            const bx=R-w-8, by=T+8;

            roundRect(ctx,bx,by,w,28,8);
            ctx.fillStyle=C.legendBg;
            ctx.fill();

            ctx.fillStyle=C.text;
            ctx.textAlign="left";
            ctx.fillText(label,bx+10,by+19);
        }
    }
}

cv.addEventListener("mousemove",e=>{
    const r=cv.getBoundingClientRect();
    hoverX=(e.clientX-r.left)*(cv._w/r.width);
    render();
});

cv.addEventListener("mouseleave",()=>{
    hoverX=null;
    render();
});

cv.addEventListener("touchmove",e=>{
    const r=cv.getBoundingClientRect();
    hoverX=(e.touches[0].clientX-r.left)*(cv._w/r.width);
    render();
},{passive:true});

cv.addEventListener("touchend",()=>{
    hoverX=null;
    render();
});

// ======================================
// RESPONSIVE RESIZING
// ======================================

function resize(){
    fit();
    render();
}

if(typeof ResizeObserver!=="undefined"){
    new ResizeObserver(resize).observe(cv.parentElement);
}
window.addEventListener("resize",resize);

// initial display
fit();
render();

})();
</script>

</div>
"""

html = html.replace("ROOT_ID", uid)

# Everything runs in the browser (JavaScript), so changing a parameter
# never triggers a Streamlit rerun.
components.html(html, height=1000, scrolling=True)
