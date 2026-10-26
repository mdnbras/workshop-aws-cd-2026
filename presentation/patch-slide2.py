from pathlib import Path
import re

path = Path(__file__).with_name("index.html")
html = path.read_text(encoding="utf-8")

new_slide = r'''<section class="slide" data-title="Síncrono vs Assíncrono — fluxo interativo">
      <style>
        #flowLab{margin-top:10px}
        #flowLab .flow-toolbar{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;margin-bottom:10px}
        #flowLab .flow-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
        #flowLab .flow-btn{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#dce8f8;border-radius:999px;padding:8px 13px;cursor:pointer;font-size:12px;font-weight:800;transition:.2s ease}
        #flowLab .flow-btn:hover,#flowLab .flow-btn.active{background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.26)}
        #flowLab .flow-btn.sync.active{color:#65d8ff;border-color:rgba(101,216,255,.45)}
        #flowLab .flow-btn.async.active{color:#ff7fc4;border-color:rgba(255,127,196,.45)}
        #flowLab .flow-stage{border:1px solid rgba(255,255,255,.12);border-radius:26px;background:rgba(7,11,22,.66);overflow:hidden;box-shadow:0 18px 48px rgba(0,0,0,.28)}
        #flowLab svg{display:block;width:100%;height:auto;max-height:48vh}
        #flowLab .wire{fill:none;stroke-width:2.3;opacity:.28;transition:opacity .2s ease,filter .2s ease}
        #flowLab .wire.sync{stroke:#54d6ff}
        #flowLab .wire.async{stroke:#ff5db1}
        #flowLab .wire.return{stroke:#49d17d;stroke-dasharray:7 7}
        #flowLab .wire.hot{opacity:1;filter:drop-shadow(0 0 5px currentColor)}
        #flowLab .flow-node-svg rect{fill:#0d1528;stroke:rgba(255,255,255,.18);stroke-width:1.4;transition:.2s ease}
        #flowLab .flow-node-svg text{fill:#f5f8ff;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;text-anchor:middle;pointer-events:none}
        #flowLab .flow-node-svg .primary{font-size:13px;font-weight:800}
        #flowLab .flow-node-svg .secondary{font-size:9.5px;font-weight:650;fill:#8fa1bb}
        #flowLab .flow-node-svg.client rect{stroke:#ff9900}
        #flowLab .flow-node-svg.api rect{stroke:#67b7ff}
        #flowLab .flow-node-svg.sync rect{stroke:#54d6ff}
        #flowLab .flow-node-svg.event rect,#flowLab .flow-node-svg.sns rect{stroke:#ff9900}
        #flowLab .flow-node-svg.queue rect{stroke:#9a7cff}
        #flowLab .flow-node-svg.worker rect{stroke:#49d17d}
        #flowLab .flow-node-svg.response rect{stroke:#49d17d;fill:rgba(73,209,125,.09)}
        #flowLab .flow-node-svg.active rect{stroke-width:2.5;filter:drop-shadow(0 0 7px rgba(255,255,255,.18))}
        #flowLab .lane-title{font:800 11px Inter,ui-sans-serif,system-ui;letter-spacing:.08em;text-transform:uppercase}
        #flowLab .lane-title.sync{fill:#7ee4ff}
        #flowLab .lane-title.async{fill:#ff91cd}
        #flowLab .lane-hint{font:600 10px Inter,ui-sans-serif,system-ui;fill:#8395b0}
        #flowLab .flow-summary{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:9px}
        #flowLab .summary-chip{display:flex;align-items:flex-start;gap:9px;padding:8px 11px;border-radius:14px;border:1px solid rgba(255,255,255,.10);background:rgba(255,255,255,.03);font-size:11px;line-height:1.35;color:#aebed3}
        #flowLab .summary-chip b{color:#eef5ff}.legend-dot{width:8px;height:8px;border-radius:50%;flex:none;margin-top:3px}
        #flowLab .packet{filter:drop-shadow(0 0 6px currentColor)}
        @media(max-height:900px){#flowLab svg{max-height:43vh}#flowLab .flow-toolbar h2{font-size:34px!important}#flowLab .flow-toolbar p{font-size:13px!important}}
      </style>

      <div class="inner">
        <span class="eyebrow"><span class="dot"></span>Resultado final</span>
        <div id="flowLab">
          <div class="flow-toolbar">
            <div>
              <h2 style="margin:6px 0 3px;font-size:clamp(30px,4vw,52px)">Do Postman ao backend: <span class="accent">dois modelos</span></h2>
              <p style="font-size:15px">As conexões agora fazem parte do mesmo SVG das caixas, mantendo tudo alinhado em qualquer resolução.</p>
            </div>
            <div class="flow-actions" aria-label="Controles da animação">
              <button class="flow-btn sync" data-run="sync">▶ Síncrono</button>
              <button class="flow-btn async" data-run="async">▶ Assíncrono</button>
              <button class="flow-btn" data-run="both">▶ Comparar</button>
              <button class="flow-btn" data-run="reset">↻ Reset</button>
            </div>
          </div>

          <div class="flow-stage">
            <svg id="flowSvg" viewBox="0 0 1120 420" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Comparação visual entre fluxo síncrono e fluxo assíncrono com SNS e SQS">
              <defs>
                <pattern id="flowGrid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="rgba(255,255,255,.035)" stroke-width="1"/></pattern>
                <marker id="arrowSync" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#54d6ff" opacity=".75"/></marker>
                <marker id="arrowAsync" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#ff5db1" opacity=".75"/></marker>
                <marker id="arrowReturn" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#49d17d" opacity=".85"/></marker>
              </defs>

              <rect x="0" y="0" width="1120" height="420" fill="url(#flowGrid)"/>
              <rect x="356" y="20" width="744" height="164" rx="22" fill="rgba(84,214,255,.025)" stroke="rgba(84,214,255,.10)"/>
              <rect x="356" y="220" width="744" height="180" rx="22" fill="rgba(255,93,177,.025)" stroke="rgba(255,93,177,.10)"/>
              <text x="378" y="43" class="lane-title sync">MODELO SÍNCRONO</text>
              <text x="378" y="243" class="lane-title async">AWS + EVENTOS</text>
              <text x="1090" y="43" text-anchor="end" class="lane-hint">cliente espera todo o encadeamento</text>
              <text x="1090" y="243" text-anchor="end" class="lane-hint">cliente é liberado; consumers seguem depois</text>

              <path id="p-entry-sync" class="wire sync" marker-end="url(#arrowSync)" d="M155 196 C175 196 188 196 210 196"/>
              <path id="p-entry-async" class="wire async" marker-end="url(#arrowAsync)" d="M155 214 C175 214 188 214 210 214"/>
              <path id="p-sync-1" class="wire sync" marker-end="url(#arrowSync)" d="M350 195 C385 195 392 102 430 102"/>
              <path id="p-sync-2" class="wire sync" marker-end="url(#arrowSync)" d="M560 102 C585 102 602 102 626 102"/>
              <path id="p-sync-3" class="wire sync" marker-end="url(#arrowSync)" d="M756 102 C781 102 798 102 822 102"/>
              <path id="p-sync-4" class="wire sync" marker-end="url(#arrowSync)" d="M952 102 C972 102 986 102 1002 102"/>

              <path id="p-async-1" class="wire async" marker-end="url(#arrowAsync)" d="M350 215 C386 215 392 295 430 295"/>
              <path id="p-async-2" class="wire async" marker-end="url(#arrowAsync)" d="M560 295 C580 295 592 295 610 295"/>
              <path id="p-async-q1" class="wire async" marker-end="url(#arrowAsync)" d="M730 295 C762 295 764 272 794 272"/>
              <path id="p-async-q2" class="wire async" marker-end="url(#arrowAsync)" d="M730 295 C762 295 764 350 794 350"/>
              <path id="p-async-w1" class="wire async" marker-end="url(#arrowAsync)" d="M914 272 C936 272 948 272 968 272"/>
              <path id="p-async-w2" class="wire async" marker-end="url(#arrowAsync)" d="M914 350 C936 350 948 350 968 350"/>
              <path id="p-return" class="wire return" marker-end="url(#arrowReturn)" d="M280 235 C280 265 280 290 280 318"/>
              <path id="p-return-client" class="wire return" marker-end="url(#arrowReturn)" d="M210 345 C178 345 142 318 118 245"/>

              <g class="flow-node-svg client" data-node="client">
                <rect x="25" y="175" width="130" height="60" rx="14"/>
                <text x="90" y="201" class="primary">POST /orders</text><text x="90" y="218" class="secondary">Postman</text>
              </g>
              <g class="flow-node-svg api" data-node="api">
                <rect x="210" y="175" width="140" height="60" rx="14"/>
                <text x="280" y="201" class="primary">Order API</text><text x="280" y="218" class="secondary">Kotlin + Spring Boot</text>
              </g>

              <g class="flow-node-svg sync" data-node="sync1">
                <rect x="430" y="72" width="130" height="60" rx="14"/>
                <text x="495" y="98" class="primary">Notification API</text><text x="495" y="115" class="secondary">HTTP síncrono</text>
              </g>
              <g class="flow-node-svg sync" data-node="sync2">
                <rect x="626" y="72" width="130" height="60" rx="14"/>
                <text x="691" y="98" class="primary">Analytics API</text><text x="691" y="115" class="secondary">HTTP síncrono</text>
              </g>
              <g class="flow-node-svg sync" data-node="sync3">
                <rect x="822" y="72" width="130" height="60" rx="14"/>
                <text x="887" y="98" class="primary">Persistência</text><text x="887" y="115" class="secondary">aguarda concluir</text>
              </g>
              <g class="flow-node-svg sync" data-node="sync4">
                <rect x="1002" y="72" width="96" height="60" rx="14"/>
                <text x="1050" y="98" class="primary">200 / 201</text><text x="1050" y="115" class="secondary">no final</text>
              </g>

              <g class="flow-node-svg event" data-node="event">
                <rect x="430" y="265" width="130" height="60" rx="14"/>
                <text x="495" y="291" class="primary">OrderCreated</text><text x="495" y="308" class="secondary">evento</text>
              </g>
              <g class="flow-node-svg sns" data-node="sns">
                <rect x="610" y="265" width="120" height="60" rx="14"/>
                <text x="670" y="291" class="primary">Amazon SNS</text><text x="670" y="308" class="secondary">fan-out</text>
              </g>
              <g class="flow-node-svg queue" data-node="q1">
                <rect x="794" y="246" width="120" height="52" rx="13"/>
                <text x="854" y="269" class="primary">notification-queue</text><text x="854" y="285" class="secondary">Amazon SQS</text>
              </g>
              <g class="flow-node-svg queue" data-node="q2">
                <rect x="794" y="324" width="120" height="52" rx="13"/>
                <text x="854" y="347" class="primary">analytics-queue</text><text x="854" y="363" class="secondary">Amazon SQS</text>
              </g>
              <g class="flow-node-svg worker" data-node="w1">
                <rect x="968" y="246" width="130" height="52" rx="13"/>
                <text x="1033" y="269" class="primary">notification-worker</text><text x="1033" y="285" class="secondary">processa depois</text>
              </g>
              <g class="flow-node-svg worker" data-node="w2">
                <rect x="968" y="324" width="130" height="52" rx="13"/>
                <text x="1033" y="347" class="primary">analytics-worker</text><text x="1033" y="363" class="secondary">processa depois</text>
              </g>
              <g class="flow-node-svg response" data-node="response">
                <rect x="210" y="318" width="140" height="54" rx="14"/>
                <text x="280" y="342" class="primary">202 Accepted</text><text x="280" y="358" class="secondary">cliente liberado</text>
              </g>
            </svg>
          </div>

          <div class="flow-summary">
            <div class="summary-chip"><span class="legend-dot" style="background:#54d6ff"></span><span><b>Síncrono:</b> Notification, Analytics e persistência fazem parte do tempo da requisição.</span></div>
            <div class="summary-chip"><span class="legend-dot" style="background:#ff5db1"></span><span><b>Assíncrono:</b> a API publica <code>OrderCreated</code>, retorna 202 e os consumidores avançam independentemente.</span></div>
          </div>
        </div>
      </div>

      <script>
      (() => {
        const root = document.getElementById('flowLab');
        const slide = root?.closest('.slide');
        const svg = document.getElementById('flowSvg');
        if (!root || !slide || !svg || root.dataset.ready) return;
        root.dataset.ready = '1';
        let runToken = 0;
        let autoPlayed = false;
        const sleep = ms => new Promise(r => setTimeout(r, ms));
        const node = name => root.querySelector(`[data-node="${name}"]`);
        const pathEl = id => root.querySelector(`#${id}`);
        const buttons = [...root.querySelectorAll('[data-run]')];

        function reset(){
          runToken++;
          root.querySelectorAll('.flow-node-svg').forEach(n => n.classList.remove('active'));
          root.querySelectorAll('.wire').forEach(w => w.classList.remove('hot'));
          root.querySelectorAll('.packet').forEach(p => p.remove());
          buttons.forEach(b => b.classList.remove('active'));
        }

        function activateNode(name){ node(name)?.classList.add('active'); }
        function heat(id){ pathEl(id)?.classList.add('hot'); }

        function animatePath(id, color, duration, token){
          return new Promise(resolve => {
            const p = pathEl(id); if (!p || token !== runToken) return resolve();
            heat(id);
            const total = p.getTotalLength();
            const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
            c.setAttribute('r','5'); c.setAttribute('fill',color); c.setAttribute('class','packet');
            svg.appendChild(c);
            const start = performance.now();
            const step = now => {
              if (token !== runToken) { c.remove(); return resolve(); }
              const t = Math.min(1,(now-start)/duration);
              const pt = p.getPointAtLength(total*t);
              c.setAttribute('cx',pt.x); c.setAttribute('cy',pt.y);
              if (t < 1) requestAnimationFrame(step); else { setTimeout(()=>c.remove(),120); resolve(); }
            };
            requestAnimationFrame(step);
          });
        }

        async function runSync(sharedEntry=true){
          const token = runToken;
          buttons.find(b=>b.dataset.run==='sync')?.classList.add('active');
          activateNode('client'); await sleep(180); if(token!==runToken)return;
          if(sharedEntry){ await animatePath('p-entry-sync','#7ee4ff',420,token); activateNode('api'); await sleep(180); }
          await animatePath('p-sync-1','#7ee4ff',620,token); activateNode('sync1'); await sleep(150);
          await animatePath('p-sync-2','#7ee4ff',420,token); activateNode('sync2'); await sleep(150);
          await animatePath('p-sync-3','#7ee4ff',420,token); activateNode('sync3'); await sleep(150);
          await animatePath('p-sync-4','#7ee4ff',420,token); activateNode('sync4');
        }

        async function runAsync(sharedEntry=true){
          const token = runToken;
          buttons.find(b=>b.dataset.run==='async')?.classList.add('active');
          activateNode('client'); await sleep(180); if(token!==runToken)return;
          if(sharedEntry){ await animatePath('p-entry-async','#ff77c1',420,token); activateNode('api'); await sleep(180); }
          await animatePath('p-async-1','#ff77c1',580,token); activateNode('event'); await sleep(120);
          await animatePath('p-async-2','#ff77c1',360,token); activateNode('sns'); await sleep(100);
          const returnPromise = (async()=>{ await animatePath('p-return','#66ea95',430,token); activateNode('response'); await animatePath('p-return-client','#66ea95',520,token); })();
          const branches = Promise.all([
            (async()=>{ await animatePath('p-async-q1','#ff77c1',460,token); activateNode('q1'); await animatePath('p-async-w1','#ff77c1',400,token); activateNode('w1'); })(),
            (async()=>{ await animatePath('p-async-q2','#ff77c1',500,token); activateNode('q2'); await animatePath('p-async-w2','#ff77c1',400,token); activateNode('w2'); })()
          ]);
          await Promise.all([returnPromise,branches]);
        }

        async function run(mode){
          reset();
          const token = runToken;
          buttons.find(b=>b.dataset.run===mode)?.classList.add('active');
          if(mode==='sync') return runSync(true);
          if(mode==='async') return runAsync(true);
          if(mode==='both'){
            activateNode('client');
            await sleep(180); if(token!==runToken)return;
            await Promise.all([
              animatePath('p-entry-sync','#7ee4ff',420,token),
              animatePath('p-entry-async','#ff77c1',420,token)
            ]);
            activateNode('api'); await sleep(160); if(token!==runToken)return;
            await Promise.all([runSync(false),runAsync(false)]);
          }
        }

        buttons.forEach(btn => btn.addEventListener('click', e => {
          e.stopPropagation();
          btn.dataset.run === 'reset' ? reset() : run(btn.dataset.run);
        }));

        const observer = new MutationObserver(() => {
          if (slide.classList.contains('active') && !autoPlayed) {
            autoPlayed = true;
            setTimeout(()=>run('both'),450);
          }
        });
        observer.observe(slide,{attributes:true,attributeFilter:['class']});
        if(slide.classList.contains('active')) setTimeout(()=>{autoPlayed=true;run('both')},450);
      })();
      </script>

      <aside class="notes">Use os botões para comparar os dois modelos. Todo o diagrama está no mesmo SVG, então as linhas ficam presas às caixas mesmo quando a apresentação é redimensionada. No síncrono, a resposta só acontece depois de Notification, Analytics e persistência. No assíncrono, OrderCreated vai ao SNS, a API retorna 202 e SNS faz fan-out para filas SQS independentes.</aside>
    </section>'''

patterns = [
    re.compile(r'<section class="slide" data-title="Objetivo do workshop">.*?</section>', re.DOTALL),
    re.compile(r'<section class="slide" data-title="Síncrono vs Assíncrono — resultado final">.*?</section>', re.DOTALL),
    re.compile(r'<section class="slide" data-title="Síncrono vs Assíncrono — fluxo interativo">.*?</section>', re.DOTALL),
]
for pattern in patterns:
    if pattern.search(html):
        html = pattern.sub(new_slide, html, count=1)
        break
else:
    raise RuntimeError("Could not locate slide 2 to replace")

path.write_text(html, encoding="utf-8")
print("Slide 2 updated with fixed SVG connections.")
