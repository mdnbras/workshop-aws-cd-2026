# Lab 4 — Consumidores independentes

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/04-consumers
```

## Estado inicial

O producer, SNS e duas filas já existem. Nesta branch entram os consumers:

```text
                         +-> notification-queue -> notification-worker
Order API -> orders-topic
                         +-> analytics-queue    -> analytics-worker
```

Ainda não existe DLQ.

## Objetivo

Executar dois consumers independentes em Kotlin e observar que cada um reage ao mesmo evento sem bloquear o outro.

## Passos

```bash
docker compose up --build -d
```

Acompanhe os logs:

```bash
docker compose logs -f notification-worker
```

```bash
docker compose logs -f analytics-worker
```

Publique um evento:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"student@aws.local","total":249.90}'
```

Pare analytics:

```bash
docker compose stop analytics-worker
```

Publique mais eventos e confirme que notification continua funcionando. Depois verifique o backlog:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/analytics-queue \
  --attribute-names ApproximateNumberOfMessages
```

Reative:

```bash
docker compose start analytics-worker
```

## Estado final

- [ ] Os dois workers processam o mesmo evento.
- [ ] Parar analytics não afeta notification.
- [ ] A fila preserva mensagens enquanto o consumer está parado.
- [ ] Ao voltar, analytics processa o backlog.

## Próxima etapa

```bash
docker compose down -v
git switch workshop/05-dlq-final
```
