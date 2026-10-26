# Lab 5 — Retry e Dead Letter Queue

Tempo sugerido: **15 minutos**.

## Branch deste laboratório

```bash
git switch workshop/05-dlq-final
```

Se estiver vindo do Lab 4:

```bash
docker compose down -v
git switch workshop/05-dlq-final
```

## Estado inicial

Todos os componentes principais já existem:

```text
                         +-> notification-queue -> notification-worker
Order API -> orders-topic
                         +-> analytics-queue    -> analytics-worker
```

Nesta etapa adicionamos uma política de redrive à fila de notificação:

```text
notification-queue
       |
       | após falhas repetidas
       v
notification-dlq
```

## Objetivo

Provocar uma falha persistente em apenas um consumidor e observar como SQS faz retry e depois move a mensagem para uma DLQ.

## 1. Confirme a branch

```bash
git branch --show-current
```

Resultado esperado:

```text
workshop/05-dlq-final
```

## 2. Suba o ambiente final

```bash
docker compose up --build -d
```

Confira:

```bash
docker compose ps
```

## 3. Abra o log de notification

```bash
docker compose logs -f notification-worker
```

## 4. Envie o evento que força falha

O handler foi preparado para falhar quando receber:

```text
fail@workshop.local
```

Envie:

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"fail@workshop.local","total":99.90}'
```

## 5. Observe os consumidores

Em outro terminal:

```bash
docker compose logs -f analytics-worker
```

O resultado esperado é:

- `analytics-worker` processa normalmente;
- `notification-worker` falha;
- a mensagem não é apagada de `notification-queue`;
- depois do Visibility Timeout, ela fica visível novamente;
- o worker tenta processá-la outra vez;
- após `maxReceiveCount`, SQS move a mensagem para `notification-dlq`.

Esse é um ponto central do workshop: **uma falha localizada não interrompe todos os consumidores**.

## 6. Entenda o Visibility Timeout

Fluxo simplificado:

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

A mensagem não some quando é recebida. Ela fica temporariamente invisível.

Se o processamento for concluído, o consumer executa `DeleteMessage`.

Se não for apagada, volta a ficar disponível.

## 7. Veja a configuração da fila

```bash
docker compose --profile tools run --rm aws-cli sqs get-queue-attributes \
  --queue-url http://floci:4566/000000000000/notification-queue \
  --attribute-names VisibilityTimeout RedrivePolicy
```

Discuta:

- `VisibilityTimeout`;
- `maxReceiveCount`;
- `deadLetterTargetArn`.

## 8. Consulte a DLQ

Depois das tentativas:

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/notification-dlq \
  --max-number-of-messages 10
```

Você deve encontrar o evento com:

```text
fail@workshop.local
```

## 9. Por que não fazer retry infinito?

Uma mensagem inválida ou uma falha permanente pode:

- consumir recursos continuamente;
- gerar ruído nos logs;
- atrasar outras mensagens;
- esconder um problema que precisa de investigação.

DLQ não corrige a mensagem. Ela **isola** o problema para tratamento posterior.

## 10. O que faríamos em produção?

Um fluxo real normalmente inclui:

1. alerta para crescimento da DLQ;
2. investigação da causa;
3. correção da aplicação ou dos dados;
4. validação da mensagem;
5. redrive ou reprocessamento controlado;
6. idempotência para evitar efeitos duplicados.

## Estado final

Você terminou com a arquitetura completa do workshop:

```text
                                   +-> notification-worker
                                   |          |
                                   |          | falha repetida
                                   |          v
Order API -> SNS -> notification-queue       DLQ
              |
              +----> analytics-queue -> analytics-worker
```

Conceitualmente:

```text
Producer
  |
  v
Topic
  |
  +-> Queue -> Consumer
  |
  +-> Queue -> Consumer
              |
              +-> retry / DLQ quando necessário
```

## Checklist de saída

- [ ] Estou na branch `workshop/05-dlq-final`.
- [ ] Consigo provocar uma falha controlada.
- [ ] Analytics continua funcionando durante a falha.
- [ ] Entendi Visibility Timeout.
- [ ] Vi a mensagem sendo tentada novamente.
- [ ] Encontrei a mensagem na DLQ.
- [ ] Sei explicar por que DLQ não substitui tratamento de erro.

## Pergunta de fixação

**Por que analytics processou o evento mesmo com notification falhando?**

Porque cada consumidor possui sua própria fila. A falha ficou isolada no fluxo de notificação.

## Próximo passo

O laboratório principal terminou. Se houver tempo, siga para [Desafios extras](07-desafios.md).

Para retornar diretamente ao estado final em qualquer momento:

```bash
git switch workshop/05-dlq-final
docker compose up --build -d
```
