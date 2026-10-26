# Lab 5 — Retry e Dead Letter Queue

Tempo sugerido: **15 minutos**.

## Branch deste laboratório

```bash
git switch workshop/05-dlq-final
```

## Estado inicial

Todos os componentes principais já existem e notification possui política de redrive para uma DLQ:

```text
                                   +-> notification-worker
                                   |          |
Order API -> SNS -> notification-queue       +-> notification-dlq
              |
              +----> analytics-queue -> analytics-worker
```

## Objetivo

Provocar uma falha persistente, observar retry via Visibility Timeout e acompanhar a mensagem até a DLQ.

## Passos

```bash
docker compose up --build -d
```

Abra os logs:

```bash
docker compose logs -f notification-worker
```

Em outro terminal:

```bash
docker compose logs -f analytics-worker
```

Envie o evento que força falha apenas em notification:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"fail@workshop.local","total":99.90}'
```

Consulte a configuração da fila:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --attribute-names VisibilityTimeout RedrivePolicy
```

Depois das tentativas, consulte a DLQ:

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/notification-dlq \
  --max-number-of-messages 10
```

## Estado final

- [ ] Analytics processou normalmente.
- [ ] Notification falhou sem apagar a mensagem.
- [ ] Vi a mensagem ser tentada novamente.
- [ ] Entendi Visibility Timeout.
- [ ] A mensagem chegou à DLQ após `maxReceiveCount`.
- [ ] Sei explicar por que DLQ isola, mas não corrige, o problema.

## Workshop concluído

Para voltar ao estado final em qualquer momento:

```bash
git switch workshop/05-dlq-final
docker compose up --build -d
```
