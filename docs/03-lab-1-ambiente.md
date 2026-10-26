# Lab 1 — Ambiente AWS local com Floci

Tempo sugerido: **15 minutos**.

## Branch deste laboratório

```bash
git switch workshop/01-floci
```

## Estado inicial

Nesta etapa ainda não existe aplicação backend, producer ou consumer. Existe apenas o ambiente Docker com Floci e AWS CLI.

```text
Docker
  +-- Floci :4566
  +-- AWS CLI
```

## Objetivo

Subir uma AWS local e manipular uma fila SQS sem conta AWS real.

## Passos

```bash
docker compose up -d floci
docker compose ps
```

Teste a CLI:

```bash
docker compose --profile tools run --rm aws-cli sts get-caller-identity
```

Crie uma fila:

```bash
docker compose --profile tools run --rm aws-cli sqs create-queue --queue-name hello-workshop
```

Envie uma mensagem:

```bash
docker compose --profile tools run --rm aws-cli sqs send-message \
  --queue-url http://floci:4566/000000000000/hello-workshop \
  --message-body '{"message":"hello event-driven world"}'
```

Receba:

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

Limpe:

```bash
docker compose --profile tools run --rm aws-cli sqs delete-queue \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

## Estado final

Você deve saber explicar o papel do Floci, o endpoint `:4566` e como uma fila mantém mensagens até que sejam consumidas.

- [ ] Floci está ativo.
- [ ] AWS CLI conversa com o ambiente local.
- [ ] Criei, enviei, recebi e removi uma fila de teste.

## Próxima etapa

```bash
docker compose down -v
git switch workshop/02-producer
```
