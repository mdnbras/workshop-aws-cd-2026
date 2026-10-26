# Lab 2 — Publicando o primeiro evento

Tempo sugerido: **20 minutos**.

## Objetivo

Receber uma requisição HTTP e publicar um evento `OrderCreated` no Amazon SNS local.

## 1. Suba todo o ambiente

```bash
docker compose up --build -d
```

Acompanhe o startup:

```bash
docker compose logs -f order-api
```

## 2. Entenda o endpoint

A API expõe:

```http
POST /orders
Content-Type: application/json
```

Payload:

```json
{
  "customerEmail": "dev@aws.local",
  "total": 149.90
}
```

O endpoint cria um `orderId`, cria um `eventId` e publica o evento no tópico SNS `orders-topic`.

## 3. Envie o primeiro pedido

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"dev@aws.local","total":149.90}'
```

Resposta esperada: HTTP `202 Accepted` com o evento criado.

## 4. Veja o log do producer

```bash
docker compose logs --tail=50 order-api
```

Procure por algo parecido com:

```text
event=OrderCreated eventId=... orderId=... published=true
```

## 5. Inspecione o tópico

```bash
docker compose --profile tools run --rm aws-cli sns list-topics
```

Você deve ver:

```text
arn:aws:sns:us-east-1:000000000000:orders-topic
```

## 6. O que o código faz?

No `OrderController`:

```java
snsClient.publish(PublishRequest.builder()
    .topicArn(topicArn)
    .message(message)
    .build());
```

O detalhe importante não é decorar a API do SDK. É entender a responsabilidade:

```text
HTTP request
   -> regra da aplicação
   -> evento criado
   -> evento publicado
```

O producer não chama notification e analytics diretamente.

## 7. Pare os consumidores e publique de novo

```bash
docker compose stop notification-worker analytics-worker
```

Publique mais dois pedidos.

Depois verifique quantas mensagens existem nas filas:

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --attribute-names ApproximateNumberOfMessages
```

Faça o mesmo para `analytics-queue`.

## Pergunta de fixação

**Por que a Order API não chama diretamente os dois workers?**

Porque o objetivo é desacoplar o producer dos consumidores. Novos consumidores podem surgir sem mudar a chamada HTTP original.

## Próximo passo

No próximo lab vamos visualizar o fan-out: um evento entrando no SNS e duas cópias independentes indo para duas filas SQS.
