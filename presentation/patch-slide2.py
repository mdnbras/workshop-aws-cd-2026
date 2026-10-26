from pathlib import Path
import re

path = Path(__file__).with_name("index.html")
html = path.read_text(encoding="utf-8")

new_slide = r'''<section class="slide" data-title="Síncrono vs Assíncrono — resultado final">
      <div class="inner">
        <span class="eyebrow"><span class="dot"></span>Resultado final</span>
        <h2 style="margin-bottom:10px">Mesmo pedido. <span class="accent">Dois jeitos de processar.</span></h2>
        <p style="font-size:19px">Do Postman ao backend: compare o modelo síncrono tradicional com o fluxo orientado a eventos na AWS.</p>

        <div class="grid-2" style="margin-top:22px;gap:18px;align-items:stretch">
          <div class="card bluebg" style="padding:20px;min-height:0">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
              <strong style="margin:0">Modelo síncrono</strong>
              <span class="pill" style="font-size:12px">cliente espera</span>
            </div>

            <div class="diagram" style="padding:18px;margin-top:16px">
              <div class="flow" style="gap:8px;flex-wrap:nowrap">
                <div class="node blue" style="min-width:96px;padding:14px 10px">Postman</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node" style="min-width:104px;padding:14px 10px">Order API</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node" style="min-width:116px;padding:14px 10px">Notification</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node" style="min-width:100px;padding:14px 10px">Analytics</div>
              </div>
              <div class="flow" style="margin-top:14px;justify-content:flex-end">
                <div style="font-size:12px;color:var(--muted)">todos precisam concluir</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node orange" style="min-width:145px;padding:11px">200 / 201<br><span style="font-size:11px;color:var(--muted)">resposta no final</span></div>
              </div>
            </div>

            <div class="list" style="gap:9px;margin-top:15px">
              <div class="list-item" style="font-size:16px"><span class="num" style="width:26px;height:26px;border-radius:9px;font-size:13px">1</span><div>O backend espera os próximos serviços terminarem.</div></div>
              <div class="list-item" style="font-size:16px"><span class="num" style="width:26px;height:26px;border-radius:9px;font-size:13px">2</span><div>Lentidão ou falha entra no caminho da requisição.</div></div>
            </div>
          </div>

          <div class="card orange" style="padding:20px;min-height:0">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
              <strong style="margin:0">Assíncrono com AWS + eventos</strong>
              <span class="pill" style="font-size:12px">desacoplado</span>
            </div>

            <div class="diagram" style="padding:18px;margin-top:16px">
              <div class="flow" style="gap:8px;flex-wrap:nowrap">
                <div class="node blue" style="min-width:88px;padding:14px 9px">Postman</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node" style="min-width:98px;padding:14px 9px">Order API</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node orange" style="min-width:108px;padding:14px 9px">OrderCreated</div>
                <div class="arrow" style="font-size:24px">→</div>
                <div class="node orange" style="min-width:78px;padding:14px 9px">SNS</div>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px">
                <div class="flow" style="gap:6px;flex-wrap:nowrap">
                  <div class="node purple" style="min-width:112px;padding:11px 8px;font-size:12px">notification-queue</div>
                  <div class="arrow" style="font-size:20px">→</div>
                  <div class="node green" style="min-width:100px;padding:11px 8px;font-size:12px">notification-worker</div>
                </div>
                <div class="flow" style="gap:6px;flex-wrap:nowrap">
                  <div class="node purple" style="min-width:106px;padding:11px 8px;font-size:12px">analytics-queue</div>
                  <div class="arrow" style="font-size:20px">→</div>
                  <div class="node green" style="min-width:96px;padding:11px 8px;font-size:12px">analytics-worker</div>
                </div>
              </div>

              <div class="flow" style="margin-top:14px;justify-content:flex-start">
                <div class="node green" style="min-width:150px;padding:11px">202 Accepted<br><span style="font-size:11px;color:var(--muted)">resposta antecipada</span></div>
                <div class="arrow" style="font-size:24px">←</div>
                <div style="font-size:12px;color:var(--muted);max-width:190px">o backend aceita o pedido; filas e workers continuam depois</div>
              </div>
            </div>

            <div class="list" style="gap:9px;margin-top:15px">
              <div class="list-item" style="font-size:16px"><span class="check" style="width:26px;height:26px">✓</span><div>O producer publica o fato e libera o cliente.</div></div>
              <div class="list-item" style="font-size:16px"><span class="check" style="width:26px;height:26px">✓</span><div>Cada consumer processa no próprio ritmo e com falha isolada.</div></div>
            </div>
          </div>
        </div>

        <div class="callout" style="margin-top:16px;padding:13px 18px;font-size:17px">
          <strong>Ideia central:</strong> no síncrono, o cliente acompanha o tempo do fluxo inteiro. No assíncrono, ele espera apenas o backend aceitar a operação e publicar o evento.
        </div>
      </div>
      <aside class="notes">Abra o workshop mostrando o resultado final. No modelo síncrono, o Postman chama a Order API e a resposta depende da conclusão de Notification e Analytics. No modelo assíncrono, a Order API publica OrderCreated no SNS, responde 202 Accepted e o processamento segue por filas SQS independentes. Reforce que o objetivo não é dizer que assíncrono é sempre melhor, e sim mostrar quando remover o acoplamento temporal faz sentido.</aside>
    </section>'''

pattern = re.compile(
    r'<section class="slide" data-title="Objetivo do workshop">.*?</section>',
    flags=re.DOTALL,
)

if pattern.search(html):
    html = pattern.sub(new_slide, html, count=1)
elif 'data-title="Síncrono vs Assíncrono — resultado final"' in html:
    print("Slide 2 already updated.")
    raise SystemExit(0)
else:
    raise RuntimeError("Could not locate slide 2 to replace")

path.write_text(html, encoding="utf-8")
print("Slide 2 updated for Pages build.")
