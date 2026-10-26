# Agenda do instrutor — 2 horas

Tema: **Construa sua primeira arquitetura orientada a eventos na AWS**  
Nível: **iniciante/intermediário**

## Resultado esperado

O participante termina o workshop conseguindo explicar e executar este fluxo:

```text
HTTP -> Producer -> SNS -> SQS -> Consumers
                         |-> SQS -> Consumer
                         |-> DLQ em caso de falha
```

## 00:00–00:15 — Fundamentos

### Fale sobre

1. Uma API normalmente chama outra API de forma síncrona.
2. Comunicação síncrona é simples, mas cria dependência de tempo e disponibilidade.
3. Um evento representa algo que **já aconteceu**: `OrderCreated`.
4. Producer não precisa conhecer todos os consumidores.
5. SNS distribui; SQS desacopla e armazena mensagens.

### Perguntas para a plateia

- Se o serviço de e-mail estiver fora, criar um pedido deve falhar?
- O serviço que cria o pedido precisa saber quantos consumidores existem?
- O que acontece se o consumidor estiver temporariamente desligado?

Não entre ainda em Kafka, EventBridge, Saga ou Event Sourcing. O objetivo é construir uma base mental simples.

---

## 00:15–00:30 — Lab 1: ambiente local

Abra [03-lab-1-ambiente.md](03-lab-1-ambiente.md).

1. Clone o repositório.
2. Rode `docker compose up floci`.
3. Explique a porta `4566`.
4. Mostre que credenciais são fictícias.
5. Crie uma fila manualmente pelo AWS CLI container.
6. Apague o recurso de teste.

**Mensagem:** estamos usando as APIs e o modelo mental da AWS, mas sem depender de conta, internet estável ou billing durante o laboratório.

---

## 00:30–00:50 — Lab 2: producer

Abra [04-lab-2-producer.md](04-lab-2-producer.md).

1. Suba todo o ambiente.
2. Mostre `OrderController`.
3. Mostre o `SnsClient` apontando para Floci.
4. Faça o primeiro `POST /orders`.
5. Pause os workers se quiser demonstrar que as mensagens permanecem nas filas.

**Mensagem:** o producer publica um fato e segue adiante.

---

## 00:50–01:15 — Lab 3: fan-out

Abra [05-lab-3-fanout.md](05-lab-3-fanout.md).

1. Mostre o tópico SNS.
2. Mostre as duas subscriptions.
3. Mostre as filas.
4. Envie um pedido.
5. Acompanhe os logs dos dois consumidores.
6. Pare `analytics-worker`, envie novos eventos e suba novamente.

**Momento importante:** o notification worker continua funcionando mesmo com analytics desligado.

---

## 01:15–01:35 — Consumidores e entrega

Explique:

- Polling da SQS.
- `VisibilityTimeout`.
- Delete somente após sucesso.
- Entrega `at-least-once`.
- Por que consumidor deve ser idempotente.

Não tente implementar idempotência completa no workshop de 2h; deixe como exercício.

---

## 01:35–01:50 — Lab 4: retry + DLQ

Abra [06-lab-4-dlq.md](06-lab-4-dlq.md).

Envie:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"fail@workshop.local","total":99.90}'
```

O notification worker falha propositalmente. A mensagem reaparece após o Visibility Timeout e, depois das tentativas configuradas, é enviada para a DLQ.

Mostre que o analytics worker processou o mesmo evento normalmente.

**Mensagem:** falha em um consumidor não precisa contaminar os demais.

---

## 01:50–02:00 — Encerramento

### Recap

Peça ao público para completar verbalmente:

- SNS serve para...
- SQS serve para...
- DLQ serve para...
- Um evento deve representar...

### Próximos passos

Mostre [07-desafios.md](07-desafios.md) e explique como a arquitetura mudaria em uma AWS real.

## Plano B para evento

Se houver problemas de rede para baixar imagens:

1. Peça que os participantes façam `docker compose pull` antes do evento.
2. Tenha as imagens Docker já baixadas na máquina do instrutor.
3. Demonstre usando apenas a máquina do instrutor se necessário.
4. Não dependa de conta AWS real para concluir o workshop.
