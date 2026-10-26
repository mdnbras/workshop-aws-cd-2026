# Lab 3 — Fan-out com SNS + SQS

Tempo sugerido: **25 minutos**.

## Objetivo

Entender como um único evento pode alimentar vários consumidores independentes.

## 1. Suba novamente os workers

```bash
docker compose start notification-worker analytics-worker
```

Abra dois terminais:

```bash
docker compose logs -f notification-worker
```

```bash
docker compose logs -f analytics-worker
```

## 2. Publique um novo pedido

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"student@aws.local","total":249.90}'
```

Você deverá ver:

```text
notification -> action=send-email
analytics    -> action=record-metric
```

O mesmo evento foi entregue a dois fluxos diferentes.

## 3. Visualize as subscriptions

```bash
docker compose --profile tools run --rm aws-cli \
  sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:us-east-1:000000000000:orders-topic
```

As duas filas estão inscritas no mesmo tópico.

## 4. Arquitetura atual

```text
                         +-> notification-queue -> notification-worker
Order API -> orders-topic
                         +-> analytics-queue    -> analytics-worker
```

SNS distribui. SQS desacopla.

## 5. Demonstre independência

Pare apenas analytics:

```bash
docker compose stop analytics-worker
```

Envie três pedidos:

```bash
for i in 1 2 3; do
  curl -s -X POST http://localhost:8080/orders \
    -H 'Content-Type: application/json' \
    -d "{\"customerEmail\":\"student${i}@aws.local\",\"total\":${i}9.90}" \
    > /dev/null
done
```

O notification worker continua processando normalmente.

Agora verifique a fila de analytics:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/analytics-queue \
  --attribute-names ApproximateNumberOfMessages
```

As mensagens ficaram esperando.

Suba analytics novamente:

```bash
docker compose start analytics-worker
```

Veja o backlog sendo processado.

## 6. Por que não usar apenas uma fila?

Imagine:

```text
                    -> notification-worker
Order API -> SQS
                    -> analytics-worker
```

Os workers competiriam pelas mensagens da mesma fila. Uma mensagem consumida e apagada por notification não ficaria disponível para analytics.

Quando **todos** os tipos de consumidores precisam receber o evento, usamos fan-out para filas independentes.

## 7. Contrato do evento

Observe o payload `OrderCreated`.

Pergunte:

- Que campos o notification worker realmente precisa?
- Que campos analytics precisa?
- O que aconteceria se renomeássemos `customerEmail`?

Eventos são contratos. Mudanças devem considerar compatibilidade com consumidores existentes.

## Pergunta de fixação

**Quem precisa conhecer todos os consumidores: Order API ou SNS?**

A Order API conhece o tópico. A configuração de subscriptions conecta os consumidores. Isso reduz acoplamento do producer.

## Próximo passo

Vamos provocar uma falha persistente e acompanhar retry + DLQ.
