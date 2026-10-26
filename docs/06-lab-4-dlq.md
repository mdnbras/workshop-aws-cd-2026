# Lab 4 — Retry e Dead Letter Queue

Tempo sugerido: **15 minutos**.

## Objetivo

Provocar uma falha persistente em apenas um consumidor e observar como SQS faz retry e, depois, move a mensagem para uma DLQ.

## 1. Garanta que tudo está executando

```bash
docker compose up -d
```

Abra o log do worker de notificação:

```bash
docker compose logs -f notification-worker
```

## 2. Envie o evento que força falha

O worker foi preparado para falhar quando receber este e-mail:

```text
fail@workshop.local
```

Envie:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"fail@workshop.local","total":99.90}'
```

## 3. Observe os dois consumidores

Em outro terminal:

```bash
docker compose logs -f analytics-worker
```

O resultado esperado é importante:

- `analytics-worker` processa normalmente.
- `notification-worker` falha.
- O evento não é apagado de `notification-queue`.
- Depois do Visibility Timeout, ele fica visível novamente.
- Após o limite de tentativas, a SQS envia a mensagem para `notification-dlq`.

Isso demonstra isolamento de falha entre consumidores.

## 4. Entenda o Visibility Timeout

A fila do workshop usa um Visibility Timeout curto para a demonstração ficar rápida.

Fluxo:

```text
receive
   |
   v
message invisible
   |
   +-- success -> delete
   |
   +-- failure -> do not delete
                    |
                    v
             visibility expires
                    |
                    v
                 retry
```

Em produção, o timeout deve ser maior que o tempo esperado de processamento e ajustado ao contexto.

## 5. Consulte a DLQ

Depois de alguns segundos:

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/notification-dlq \
  --max-number-of-messages 10
```

Você deverá encontrar o evento com `fail@workshop.local`.

## 6. Por que não fazer retry infinito?

Porque uma mensagem inválida ou uma falha permanente pode:

- consumir recursos continuamente;
- poluir logs;
- atrasar outras mensagens;
- esconder um problema que precisa de investigação humana.

DLQ não resolve a causa da falha. Ela **isola** a mensagem problemática.

## 7. O que faríamos depois em produção?

Algumas opções:

1. Gerar alarme quando a DLQ receber mensagens.
2. Investigar o motivo da falha.
3. Corrigir dados ou aplicação.
4. Reprocessar a mensagem com segurança.
5. Garantir idempotência antes do redrive.

## Pergunta de fixação

**Por que analytics processou o evento mesmo com notification falhando?**

Porque cada consumidor tem sua própria fila. A falha ficou isolada no fluxo de notificação.

## Resultado do workshop

Você construiu:

```text
                    +-> SQS -> notification worker -> DLQ
Order API -> SNS ---+
                    +-> SQS -> analytics worker
```

Essa é a base de muitas arquiteturas orientadas a eventos na AWS.
