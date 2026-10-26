# Lab 3 — Fan-out com SNS + SQS

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/03-fanout
```

Se estiver vindo do Lab 2:

```bash
docker compose down -v
git switch workshop/03-fanout
```

## Estado inicial

Nesta etapa o producer já existe e o SNS já recebe `OrderCreated`.

A novidade desta branch é a infraestrutura de fan-out:

```text
                         +-> notification-queue
Order API -> orders-topic
                         +-> analytics-queue
```

Ainda não existem consumers executando. Isso é proposital: primeiro vamos enxergar o fan-out apenas pela infraestrutura.

## Objetivo

Entender como um único evento publicado no SNS gera mensagens independentes em duas filas SQS.

## 1. Confirme a branch

```bash
git branch --show-current
```

Resultado esperado:

```text
workshop/03-fanout
```

## 2. Suba o ambiente

```bash
docker compose up --build -d
```

## 3. Veja o tópico e as filas

```bash
docker compose --profile tools run --rm aws-cli sns list-topics
```

```bash
docker compose --profile tools run --rm aws-cli sqs list-queues
```

Você deve encontrar:

```text
orders-topic
notification-queue
analytics-queue
```

## 4. Visualize as subscriptions

```bash
docker compose --profile tools run --rm aws-cli \
  sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:us-east-1:000000000000:orders-topic
```

As duas filas devem estar inscritas no mesmo tópico.

## 5. Publique um novo pedido

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"student@aws.local","total":249.90}'
```

## 6. Verifique o fan-out sem consumers

Consulte a fila de notificação:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --attribute-names ApproximateNumberOfMessages
```

Agora analytics:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/analytics-queue \
  --attribute-names ApproximateNumberOfMessages
```

O mesmo evento deve existir de forma independente nas duas filas.

## 7. Leia uma mensagem manualmente

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --max-number-of-messages 1
```

Observe o payload `OrderCreated`.

## 8. Por que não usar apenas uma fila?

Se dois tipos de consumidores compartilhassem a mesma fila, eles competiriam pelas mensagens.

```text
                    -> consumer A
Order API -> SQS
                    -> consumer B
```

Uma mensagem processada por A não seria também entregue a B.

Quando diferentes funcionalidades precisam reagir ao mesmo evento, o fan-out cria cópias independentes:

```text
SNS
 +-> SQS A
 +-> SQS B
```

SNS distribui. SQS desacopla e armazena.

## Estado final

A arquitetura agora é:

```text
                         +-> notification-queue
POST /orders -> API -> SNS
                         +-> analytics-queue
```

Nenhuma aplicação consumer está rodando ainda.

Você deve ter entendido:

- diferença entre topic e queue;
- o que significa fan-out;
- por que cada consumer costuma ter sua própria fila;
- como SNS e SQS têm responsabilidades diferentes.

## Checklist de saída

- [ ] Estou na branch `workshop/03-fanout`.
- [ ] O tópico `orders-topic` existe.
- [ ] Existem duas filas SQS.
- [ ] As duas filas estão inscritas no tópico.
- [ ] Um único `POST /orders` gera mensagem nas duas filas.

## Pergunta de fixação

**Quem precisa conhecer todos os consumidores: a Order API ou a infraestrutura de subscriptions?**

A Order API conhece apenas o tópico. As subscriptions determinam quais filas receberão cada evento.

## Próximo passo

Agora vamos adicionar aplicações que realmente consomem essas filas.

```bash
git switch workshop/04-consumers
```

Continue em [Lab 4 — Consumidores independentes](06-lab-4-consumers.md).
