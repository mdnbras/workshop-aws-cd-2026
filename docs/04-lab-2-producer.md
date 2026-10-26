# Lab 2 — Publicando o primeiro evento

Tempo sugerido: **20 minutos**.

## Branch deste laboratório

```bash
git switch workshop/02-producer
```

## Estado inicial

Nesta etapa temos apenas o producer e o tópico SNS:

```text
POST /orders -> Order API -> orders-topic
```

Ainda não existem filas ou consumers.

## Objetivo

Receber uma requisição HTTP e publicar `OrderCreated` no SNS local usando Kotlin + Spring Boot.

## Passos

```bash
docker compose up --build -d
docker compose logs -f order-api
```

Envie um pedido:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"dev@aws.local","total":149.90}'
```

Inspecione o tópico:

```bash
docker compose --profile tools run --rm aws-cli sns list-topics
```

Fluxo do código:

```text
OrderController
  -> CreateOrderService
  -> OrderCreated
  -> OrderEventPublisher
  -> SnsOrderEventPublisher
```

## Estado final

```text
HTTP -> Kotlin/Spring Boot -> OrderCreated -> SNS
```

- [ ] `POST /orders` retorna `202`.
- [ ] `orders-topic` existe.
- [ ] Vejo `OrderCreated` nos logs.
- [ ] Sei explicar por que o producer não conhece consumers.

## Próxima etapa

```bash
docker compose down -v
git switch workshop/03-fanout
```
