# Lab 2 — Publicando o primeiro evento

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/02-producer
```

Se estiver vindo do Lab 1:

```bash
docker compose down -v
git switch workshop/02-producer
```

## Estado inicial

Agora o projeto já possui:

```text
Order API (Kotlin + Spring Boot)
        |
        v
Amazon SNS local
        |
        X
   sem consumers
```

Nesta etapa ainda não existem filas SQS conectadas ao tópico. O foco é entender **producer + evento + publicação**.

## Objetivo

Receber uma requisição HTTP e publicar um evento `OrderCreated` no Amazon SNS local usando Kotlin + Spring Boot.

## 1. Confirme a branch

```bash
git branch --show-current
```

Resultado esperado:

```text
workshop/02-producer
```

## 2. Suba o ambiente

```bash
docker compose up --build -d
```

Acompanhe o startup:

```bash
docker compose logs -f order-api
```

## 3. Entenda o endpoint

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

## 4. Envie o primeiro pedido

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"dev@aws.local","total":149.90}'
```

Resposta esperada: HTTP `202 Accepted` com o evento criado.

## 5. Veja o log do producer

```bash
docker compose logs --tail=50 order-api
```

Procure por algo parecido com:

```text
event=OrderCreated eventId=... orderId=... published=true
```

## 6. Inspecione o tópico

```bash
docker compose --profile tools run --rm aws-cli sns list-topics
```

Você deve ver:

```text
arn:aws:sns:us-east-1:000000000000:orders-topic
```

## 7. O que o código faz?

O fluxo do producer está separado por responsabilidade:

```text
OrderController
      |
      v
CreateOrderService
      |
      v
OrderCreated
      |
      v
OrderEventPublisher
      |
      v
SnsOrderEventPublisher
```

O controller recebe HTTP. O service cria o evento. O publisher conhece SNS.

O ponto principal é que o código de regra não precisa conhecer detalhes do AWS SDK.

## Estado final

Ao terminar este laboratório, a arquitetura é:

```text
POST /orders
     |
     v
Order API
     |
     | OrderCreated
     v
orders-topic (SNS)
```

Ainda não há filas ou consumidores.

Você deve ter entendido:

- o papel de um producer;
- o que é um evento de negócio;
- a diferença entre `eventId` e `orderId`;
- por que a aplicação publica no tópico em vez de chamar outro serviço diretamente.

## Checklist de saída

- [ ] Estou na branch `workshop/02-producer`.
- [ ] `order-api` sobe com Docker.
- [ ] `POST /orders` retorna `202`.
- [ ] O tópico `orders-topic` existe.
- [ ] Vejo `OrderCreated` sendo publicado nos logs.

## Pergunta de fixação

**Por que a Order API publica um evento em vez de chamar diretamente notification ou analytics?**

Porque o producer deve comunicar o que aconteceu, sem precisar conhecer quem vai reagir ao evento.

## Próximo passo

Agora vamos conectar o SNS a duas filas independentes.

```bash
git switch workshop/03-fanout
```

Continue em [Lab 3 — Fan-out com SNS + SQS](05-lab-3-fanout.md).
