# Lab 4 — Consumidores independentes

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/04-consumers
```

Se estiver vindo do Lab 3:

```bash
docker compose down -v
git switch workshop/04-consumers
```

## Estado inicial

A arquitetura já possui producer, SNS e duas filas SQS.

Nesta branch entram os consumers:

```text
                         +-> notification-queue -> notification-worker
Order API -> orders-topic
                         +-> analytics-queue    -> analytics-worker
```

A DLQ ainda não faz parte desta etapa.

## Objetivo

Executar dois consumidores independentes em Kotlin e observar que cada um reage ao mesmo evento de forma diferente.

## 1. Confirme a branch

```bash
git branch --show-current
```

Resultado esperado:

```text
workshop/04-consumers
```

## 2. Suba todo o ambiente

```bash
docker compose up --build -d
```

## 3. Acompanhe os logs dos consumidores

Em um terminal:

```bash
docker compose logs -f notification-worker
```

Em outro:

```bash
docker compose logs -f analytics-worker
```

## 4. Publique um evento

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"student@aws.local","total":249.90}'
```

Você deverá ver comportamentos diferentes para o mesmo evento:

```text
notification -> action=send-email
analytics    -> action=record-metric
```

## 5. Entenda a estrutura do worker

O worker está separado em responsabilidades simples:

```text
SqsOrderEventConsumer
        |
        v
OrderCreatedEvent
        |
        v
OrderCreatedHandler
```

O consumer conhece SQS e cuida de receber/apagar mensagens.

O handler contém a reação ao evento.

A mesma aplicação é executada duas vezes com configurações diferentes:

```text
WORKER_NAME=notification
WORKER_NAME=analytics
```

Isso permite ensinar consumidores diferentes sem duplicar todo o projeto.

## 6. Demonstre independência

Pare apenas analytics:

```bash
docker compose stop analytics-worker
```

Publique três pedidos:

```bash
for i in 1 2 3; do
  curl -s -X POST http://localhost:8080/orders \
    -H 'Content-Type: application/json' \
    -d "{\"customerEmail\":\"student${i}@aws.local\",\"total\":${i}9.90}" \
    > /dev/null
done
```

O `notification-worker` continua processando.

Verifique a fila de analytics:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/analytics-queue \
  --attribute-names ApproximateNumberOfMessages
```

As mensagens devem permanecer aguardando.

## 7. Reative analytics

```bash
docker compose start analytics-worker
```

Acompanhe:

```bash
docker compose logs -f analytics-worker
```

Você verá o backlog sendo processado.

## Estado final

A arquitetura é:

```text
                         +-> SQS -> notification-worker
Order API -> SNS --------+
                         +-> SQS -> analytics-worker
```

Você deve ter entendido:

- cada fila acumula mensagens independentemente;
- desligar um consumer não interrompe o outro;
- consumidores podem escalar separadamente;
- o producer não precisa conhecer nenhum worker.

## Checklist de saída

- [ ] Estou na branch `workshop/04-consumers`.
- [ ] Os dois workers iniciam corretamente.
- [ ] Um evento é processado pelos dois.
- [ ] Parar analytics não afeta notification.
- [ ] O backlog fica armazenado na fila.
- [ ] Ao reiniciar analytics, o backlog é consumido.

## Pergunta de fixação

**Se o analytics-worker ficar fora do ar por alguns minutos, notification precisa parar também?**

Não. Cada consumer possui sua própria fila e progride de forma independente.

## Próximo passo

Agora vamos introduzir falhas, retry, Visibility Timeout e Dead Letter Queue.

```bash
git switch workshop/05-dlq-final
```

Continue em [Lab 5 — Retry e Dead Letter Queue](07-lab-5-dlq.md).
