# Lab 3 — Fan-out com SNS + SQS

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/03-fanout
```

## Estado inicial

```text
Order API -> orders-topic
```

Nesta branch entram duas filas e duas subscriptions:

```text
                         +-> notification-queue
Order API -> orders-topic
                         +-> analytics-queue
```

Ainda não existem consumers.

## Objetivo

Entender fan-out e comprovar que um único evento gera mensagens independentes em duas filas SQS.

## Passos

```bash
docker compose up --build -d
```

Inspecione os recursos:

```bash
docker compose --profile tools run --rm aws-cli sns list-topics
docker compose --profile tools run --rm aws-cli sqs list-queues
```

Veja as subscriptions:

```bash
docker compose --profile tools run --rm aws-cli sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:us-east-1:000000000000:orders-topic
```

Publique:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"student@aws.local","total":249.90}'
```

Confira a quantidade de mensagens nas duas filas:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --attribute-names ApproximateNumberOfMessages
```

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/analytics-queue \
  --attribute-names ApproximateNumberOfMessages
```

## Estado final

```text
SNS
 +-> notification-queue
 +-> analytics-queue
```

- [ ] Duas filas existem.
- [ ] As duas estão inscritas no mesmo tópico.
- [ ] Um único evento chega às duas filas.
- [ ] Sei explicar por que uma única fila faria consumers competirem.

## Próxima etapa

```bash
docker compose down -v
git switch workshop/04-consumers
```
