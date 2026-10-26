from pathlib import Path
import re

path = Path(__file__).with_name("index.html")
html = path.read_text(encoding="utf-8")

new_slide = r'''<section class="slide" data-title="Síncrono vs Assíncrono — fluxo interativo">
      <style>
        #flowLab{margin-top:14px}
        #flowLab .flow-toolbar{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:10px}
        #flowLab .flow-actions{display:flex;gap:8px;flex-wrap:wrap}
        #flowLab .flow-btn{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#dce8f8;border-radius:999px;padding:8px 13px;cursor:pointer;font-size:13px;font-weight:800;transition:.2s ease}
        #flowLab .flow-btn:hover,#flowLab .flow-btn.active{transform:translateY(-1px);background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.26)}
        #flowLab .flow-btn.sync.active{color:#65d8ff;border-color:rgba(101,216,255,.45);box-shadow:0 0 26px rgba(101,216,255,.12)}
        #flowLab .flow-btn.async.active{color:#ff7fc4;border-color:rgba(255,127,196,.45);box-shadow:0 0 26px rgba(255,127,196,.12)}
        #flowLab .flow-stage{position:relative;height:430px;border:1px solid rgba(255,255,255,.12);border-radius:30px;background:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px),radial-gradient(circle at 15% 50%,rgba(103,183,255,.11),transparent 23%),radial-gradient(circle at 68% 72%,rgba(255,127,196,.08),transparent 25%),rgba(7,11,22,.64);background-size:48px 48px,48px 48px,auto,auto,auto;overflow:hidden;box-shadow:0 22px 60px rgba(0,0,0,.32)}
        #flowLab .lane-label{position:absolute;left:382px;padding:6px 10px;border-radius:999px;font-size:11px;font-weight:900;letter-spacing:.05em;text-transform:uppercase;z-index:4}
        #flowLab .lane-label.sync{top:16px;color:#7ee4ff;border:1px solid rgba(101,216,255,.28);background:rgba(101,216,255,.08)}
        #flowLab .lane-label.async{top:224px;color:#ff91cd;border:1px solid rgba(255,127,196,.28);background:rgba(255,127,196,.08)}
        #flowLab .flow-node{position:absolute;z-index:5;min-width:110px;padding:11px 13px;border-radius:16px;border:1px solid rgba(255,255,255,.14);background:rgba(11,17,32,.92);text-align:center;box-shadow:0 14px 34px rgba(0,0,0,.30);transition:.25s ease}
        #flowLab .flow-node small{display:block;margin-top:3px;color:#8fa1bb;font-size:10px;font-weight:700}
        #flowLab .flow-node b{font-size:13px;letter-spacing:-.01em}
        #flowLab .flow-node.client{left:26px;top:171px;border-color:rgba(255,153,0,.38)}
        #flowLab .flow-node.api{left:184px;top:171px;border-color:rgba(103,183,255,.38)}
        #flowLab .flow-node.sync1{left:382px;top:55px;border-color:rgba(101,216,255,.36)}
        #flowLab .flow-node.sync2{left:562px;top:55px;border-color:rgba(101,216,255,.36)}
        #flowLab .flow-node.sync3{left:742px;top:55px;border-color:rgba(101,216,255,.36)}
        #flowLab .flow-node.sync4{left:922px;top:55px;border-color:rgba(255,209,102,.40)}
        #flowLab .flow-node.event{left:382px;top:270px;border-color:rgba(255,153,0,.40)}
        #flowLab .flow-node.sns{left:542px;top:270px;border-color:rgba(255,153,0,.46)}
        #flowLab .flow-node.q1{left:714px;top:232px;border-color:rgba(154,124,255,.48)}
        #flowLab .flow-node.q2{left:714px;top:327px;border-color:rgba(154,124,255,.48)}
        #flowLab .flow-node.w1{left:904px;top:232px;border-color:rgba(73,209,125,.45)}
        #flowLab .flow-node.w2{left:904px;top:327px;border-color:rgba(73,209,125,.45)}
        #flowLab .flow-node.response{left:184px;top:315px;border-color:rgba(73,209,125,.50);background:rgba(73,209,125,.08)}
        #flowLab .flow-node.active{transform:translateY(-3px) scale(1.025);filter:brightness(1.2)}
        #flowLab .flow-node.sync-glow{box-shadow:0 0 26px rgba(101,216,255,.23),0 14px 34px rgba(0,0,0,.3)}
        #flowLab .flow-node.async-glow{box-shadow:0 0 26px rgba(255,127,196,.20),0 14px 34px rgba(0,0,0,.3)}
        #flowLab .flow-node.good-glow{box-shadow:0 0 28px rgba(73,209,125,.25),0 14px 34px rgba(0,0,0,.3)}
        #flowLab svg{position:absolute;inset:0;width:100%;height:100%;z-index:2}
        #flowLab .wire{fill:none;stroke-width:2.3;opacity:.28;transition:opacity .25s ease,filter .25s ease}
        #flowLab .wire.sync{stroke:#54d6ff}
        #flowLab .wire.async{stroke:#ff5db1}
        #flowLab .wire.return{stroke:#49d17d;stroke-dasharray:6 7}
        #flowLab .wire.hot{opacity:1;filter:drop-shadow(0 0 5px currentColor)}
        #flowLab .packet{opacity:0}
        #flowLab .packet.sync{fill:#7ee4ff}
        #flowLab .packet.async{fill:#ff77c1}
        #flowLab .packet.return{fill:#66ea95}
        #flowLab .flow-caption{position:absolute;z-index:6;font-size:11px;color:#9cafc8;max-width:190px;line-height:1.3}
        #flowLab .cap-sync{left:914px;top:119px;text-align:center}
        #flowLab .cap-async{left:374px;top:350px;color:#7ee8a3}
        #flowLab .flow-summary{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
        #flowLab .summary-chip{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:16px;border:1px solid rgba(255,255,255,.10);background:rgba(255,255,255,.035);font-size:12px;color:#b8c6da}
        #flowLab .summary-chip b{color:#eef5ff}.legend-dot{width:9px;height:9px;border-radius:50%;flex:none}
      </style>

      <div class="inner">
        <span class="eyebrow"><span class="dot"></span>Resultado final</span>
        <div id="flowLab">
          <div class="flow-toolbar">
            <div>
              <h2 style="margin:8px 0 3px;font-size:clamp(32px,4.4vw,58px)">Do Postman ao backend: <span class="accent">dois modelos</span></h2>
              <p style="font-size:16px">Dispare o fluxo e acompanhe a requisição percorrendo cada arquitetura.</p>
            </div>
            <div class="flow-actions" aria-label="Controles da animação">
              <button class="flow-btn sync" data-run="sync">▶ Síncrono</button>
              <button class="flow-btn async" data-run="async">▶ Assíncrono</button>
              <button class="flow-btn" data-run="both">▶ Comparar</button>
              <button class="flow-btn" data-run="reset">↻</button>
            </div>
          </div>

          <div class="flow-stage">
            <div class="lane-label sync">modelo síncrono</div>
            <div class="lane-label async">AWS + eventos</div>
            <svg viewBox="0 0 1120 430" preserveAspectRatio="none" aria-hidden="true">
              <path id="p-entry" class="wire sync" d="M126 198 C148 198 164 198 184 198"/>
              <path id="p-entry-a" class="wire async" d="M126 214 C148 214 164 214 184 214"/>
              <path id="p-sync-1" class="wire sync" d="M294 190 C332 190 336 80 382 80"/>
              <path id="p-sync-2" class="wire sync" d="M492 80 C518 80 538 80 562 80"/>
              <path id="p-sync-3" class="wire sync" d="M672 80 C698 80 718 80 742 80"/>
              <path id="p-sync-4" class="wire sync" d="M852 80 C878 80 898 80 922 80"/>
              <path id="p-async-1" class="wire async" d="M294 214 C330 214 338 295 382 295"/>
              <path id="p-async-2" class="wire async" d="M492 295 C510 295 526 295 542 295"/>
              <path id="p-async-q1" class="wire async" d="M652 295 C681 295 684 257 714 257"/>
              <path id="p-async-q2" class="wire async" d="M652 295 C681 295 684 352 714 352"/>
              <path id="p-async-w1" class="wire async" d="M824 257 C852 257 876 257 904 257"/>
              <path id="p-async-w2" class="wire async" d="M824 352 C852 352 876 352 904 352"/>
              <path id="p-return" class="wire return" d="M438 329 C370 401 262 396 238 350 C216 309 228 260 246 221"/>

              <circle class="packet sync" r="5"><animateMotion data-motion="sync" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-entry"/></animateMotion></circle>
              <circle class="packet sync" r="5"><animateMotion data-motion="sync" dur=".70s" begin="indefinite" fill="freeze"><mpath href="#p-sync-1"/></animateMotion></circle>
              <circle class="packet sync" r="5"><animateMotion data-motion="sync" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-sync-2"/></animateMotion></circle>
              <circle class="packet sync" r="5"><animateMotion data-motion="sync" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-sync-3"/></animateMotion></circle>
              <circle class="packet sync" r="5"><animateMotion data-motion="sync" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-sync-4"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-entry-a"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".66s" begin="indefinite" fill="freeze"><mpath href="#p-async-1"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".40s" begin="indefinite" fill="freeze"><mpath href="#p-async-2"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-async-q1"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-async-q2"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-async-w1"/></animateMotion></circle>
              <circle class="packet async" r="5"><animateMotion data-motion="async" dur=".48s" begin="indefinite" fill="freeze"><mpath href="#p-async-w2"/></animateMotion></circle>
              <circle class="packet return" r="5"><animateMotion data-motion="return" dur=".78s" begin="indefinite" fill="freeze"><mpath href="#p-return"/></animateMotion></circle>
            </svg>

            <div class="flow-node client" data-node="client"><b>POST /orders</b><small>Postman</small></div>
            <div class="flow-node api" data-node="api"><b>Order API</b><small>Kotlin + Spring Boot</small></div>
            <div class="flow-node sync1" data-node="sync1"><b>Notification API</b><small>HTTP síncrono</small></div>
            <div class="flow-node sync2" data-node="sync2"><b>Analytics API</b><small>HTTP síncrono</small></div>
            <div class="flow-node sync3" data-node="sync3"><b>Persistência</b><small>aguarda concluir</small></div>
            <div class="flow-node sync4" data-node="sync4"><b>200 / 201</b><small>resposta no final</small></div>
            <div class="flow-caption cap-sync">O cliente fica preso ao tempo de todo o encadeamento.</div>
            <div class="flow-node event" data-node="event"><b>OrderCreated</b><small>evento</small></div>
            <div class="flow-node sns" data-node="sns"><b>Amazon SNS</b><small>fan-out</small></div>
            <div class="flow-node q1" data-node="q1"><b>notification-queue</b><small>Amazon SQS</small></div>
            <div class="flow-node q2" data-node="q2"><b>analytics-queue</b><small>Amazon SQS</small></div>
            <div class="flow-node w1" data-node="w1"><b>notification-worker</b><small>processa depois</small></div>
            <div class="flow-node w2" data-node="w2"><b>analytics-worker</b><small>processa depois</small></div>
            <div class="flow-node response" data-node="response"><b>202 Accepted</b><small>cliente liberado</small></div>
            <div class="flow-caption cap-async">A resposta volta cedo; filas e workers continuam.</div>
          </div>

          <div class="flow-summary">
            <div class="summary-chip"><span class="legend-dot" style="background:#54d6ff"></span><span><b>Síncrono:</b> latência e disponibilidade dos próximos serviços entram no caminho crítico.</span></div>
            <div class="summary-chip"><span class="legend-dot" style="background:#ff5db1"></span><span><b>Assíncrono:</b> publica o fato, responde e os consumidores seguem de forma independente.</span></div>
          </div>
        </div>
      </div>

      <script>
        (() => {
          const root = document.getElementById('flowLab');
          if (!root || root.dataset.ready === '1') return;
          root.dataset.ready = '1';
          const buttons = [...root.querySelectorAll('[data-run]')];
          const node = name => root.querySelector(`[data-node="${name}"]`);
          const wires = mode => [...root.querySelectorAll(`.wire.${mode}`)];
          const motions = mode => [...root.querySelectorAll(`animateMotion[data-motion="${mode}"]`)];
          let timers = [];
          const later = (ms, fn) => timers.push(setTimeout(fn, ms));
          const clearTimers = () => { timers.forEach(clearTimeout); timers = []; };
          const activate = (name, cls) => { const n=node(name); if(n){n.classList.add('active'); if(cls)n.classList.add(cls);} };
          const reset = () => {
            clearTimers();
            buttons.forEach(b=>b.classList.remove('active'));
            root.querySelectorAll('.flow-node').forEach(n=>n.classList.remove('active','sync-glow','async-glow','good-glow'));
            root.querySelectorAll('.wire').forEach(w=>w.classList.remove('hot'));
            root.querySelectorAll('.packet').forEach(p=>p.style.opacity='0');
          };
          const runMotions = (mode,start=0,step=470) => motions(mode).forEach((m,i)=>later(start+i*step,()=>{
            m.parentElement.style.opacity='1';
            try{m.beginElement();}catch(_){ }
            later(parseFloat(m.getAttribute('dur'))*1000+50,()=>m.parentElement.style.opacity='0');
          }));
          const runSync = () => {
            reset(); buttons.find(b=>b.dataset.run==='sync')?.classList.add('active'); wires('sync').forEach(w=>w.classList.add('hot'));
            ['client','api','sync1','sync2','sync3','sync4'].forEach((n,i)=>later(i*480,()=>activate(n,'sync-glow'))); runMotions('sync',0,480);
          };
          const runAsync = () => {
            reset(); buttons.find(b=>b.dataset.run==='async')?.classList.add('active'); wires('async').forEach(w=>w.classList.add('hot')); wires('return').forEach(w=>w.classList.add('hot'));
            activate('client','async-glow'); later(440,()=>activate('api','async-glow')); later(900,()=>activate('event','async-glow')); later(1300,()=>activate('sns','async-glow'));
            later(1680,()=>{activate('q1','async-glow');activate('q2','async-glow');}); later(2110,()=>{activate('w1','good-glow');activate('w2','good-glow');}); later(1350,()=>activate('response','good-glow'));
            runMotions('async',0,420); runMotions('return',1280,420);
          };
          const runBoth = () => {
            reset(); buttons.find(b=>b.dataset.run==='both')?.classList.add('active'); wires('sync').forEach(w=>w.classList.add('hot')); wires('async').forEach(w=>w.classList.add('hot')); wires('return').forEach(w=>w.classList.add('hot'));
            activate('client','sync-glow'); later(380,()=>activate('api','sync-glow'));
            ['sync1','sync2','sync3','sync4'].forEach((n,i)=>later(760+i*430,()=>activate(n,'sync-glow')));
            later(760,()=>activate('event','async-glow')); later(1120,()=>activate('sns','async-glow')); later(1480,()=>{activate('q1','async-glow');activate('q2','async-glow');}); later(1880,()=>{activate('w1','good-glow');activate('w2','good-glow');}); later(1170,()=>activate('response','good-glow'));
            runMotions('sync',0,430); runMotions('async',0,380); runMotions('return',1110,380);
          };
          buttons.forEach(btn=>btn.addEventListener('click',e=>{e.stopPropagation(); const m=btn.dataset.run; if(m==='sync')runSync(); else if(m==='async')runAsync(); else if(m==='both')runBoth(); else reset();}));
          const slide=root.closest('.slide');
          if(slide){const observer=new MutationObserver(()=>{if(slide.classList.contains('active')&&slide.dataset.flowPlayed!=='1'){slide.dataset.flowPlayed='1';later(600,runBoth);}});observer.observe(slide,{attributes:true,attributeFilter:['class']});if(slide.classList.contains('active'))later(600,runBoth);}
        })();
      </script>
      <aside class="notes">Use Comparar para rodar os dois caminhos. No síncrono, mostre que o Postman só recebe resposta depois de Notification, Analytics e persistência. No assíncrono, mostre OrderCreated entrando no SNS, o fan-out para duas filas SQS e o 202 Accepted voltando antes dos workers terminarem. Os botões permitem repetir cada fluxo isoladamente.</aside>
    </section>'''

pattern = re.compile(
    r'<section class="slide" data-title="(?:Objetivo do workshop|Síncrono vs Assíncrono — resultado final|Síncrono vs Assíncrono — fluxo interativo)">.*?</section>',
    flags=re.DOTALL,
)

if not pattern.search(html):
    raise RuntimeError("Could not locate slide 2 to replace")

html = pattern.sub(new_slide, html, count=1)
path.write_text(html, encoding="utf-8")
print("Interactive slide 2 updated for Pages build.")
