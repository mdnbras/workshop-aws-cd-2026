# Lab 1 — Ambiente AWS local com Floci

Tempo sugerido: **15 minutos**.

## Objetivo

Subir um ambiente AWS local e executar comandos AWS sem conta real.

## 1. Suba apenas o Floci

```bash
docker compose up -d floci
```

Confira:

```bash
docker compose ps
```

O Floci publica as APIs AWS locais em:

```text
http://localhost:4566
```

## 2. Teste a AWS CLI em container

```bash
docker compose --profile tools run --rm aws-cli sts get-caller-identity
```

O resultado usa a conta local padrão `000000000000`.

## 3. Crie uma fila manualmente

```bash
docker compose --profile tools run --rm aws-cli \
  sqs create-queue --queue-name hello-workshop
```

Liste filas:

```bash
docker compose --profile tools run --rm aws-cli sqs list-queues
```

## 4. Envie uma mensagem

```bash
docker compose --profile tools run --rm aws-cli sqs send-message \
  --queue-url http://floci:4566/000000000000/hello-workshop \
  --message-body '{"message":"hello event-driven world"}'
```

## 5. Receba a mensagem

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

## 6. Limpe o recurso de teste

```bash
docker compose --profile tools run --rm aws-cli sqs delete-queue \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

## O que acabou de acontecer?

Você usou comandos do AWS CLI, mas o endpoint foi o Floci rodando no Docker.

Em uma AWS real, o endpoint seria o endpoint oficial do serviço e as credenciais seriam reais.

## Pergunta de fixação

**Se o consumer estiver desligado quando a mensagem chega à SQS, a mensagem precisa ser perdida?**

Resposta: não. A fila existe justamente para armazenar a mensagem até que um consumidor possa processá-la, respeitando as políticas de retenção configuradas.

## Próximo passo

Agora vamos deixar de publicar mensagens manualmente e criar um producer em Java/Spring Boot.
