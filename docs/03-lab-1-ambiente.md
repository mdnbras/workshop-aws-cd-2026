# Lab 1 — Ambiente AWS local com Floci

Tempo sugerido: **15 minutos**.

## Branch deste laboratório

```bash
git switch workshop/01-floci
```

Se você veio de outra etapa e quer garantir um ambiente limpo:

```bash
docker compose down -v
git switch workshop/01-floci
docker compose pull
```

## Estado inicial

Neste ponto ainda não existe aplicação backend, producer ou consumer.

O projeto contém apenas o necessário para experimentar uma AWS local:

```text
Docker Compose
   |
   +-- Floci :4566
   |
   +-- AWS CLI (profile tools)
```

Você deve ter:

- Docker em execução;
- repositório clonado;
- branch `workshop/01-floci` selecionada;
- nenhuma conta AWS necessária.

## Objetivo

Subir um ambiente AWS local e executar comandos AWS sem conta real.

## 1. Confirme a branch

```bash
git branch --show-current
```

Resultado esperado:

```text
workshop/01-floci
```

## 2. Suba apenas o Floci

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

## 3. Teste a AWS CLI em container

```bash
docker compose --profile tools run --rm aws-cli sts get-caller-identity
```

O resultado usa a conta local padrão `000000000000`.

## 4. Crie uma fila manualmente

```bash
docker compose --profile tools run --rm aws-cli \
  sqs create-queue --queue-name hello-workshop
```

Liste filas:

```bash
docker compose --profile tools run --rm aws-cli sqs list-queues
```

## 5. Envie uma mensagem

```bash
docker compose --profile tools run --rm aws-cli sqs send-message \
  --queue-url http://floci:4566/000000000000/hello-workshop \
  --message-body '{"message":"hello event-driven world"}'
```

## 6. Receba a mensagem

```bash
docker compose --profile tools run --rm aws-cli sqs receive-message \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

## 7. Limpe o recurso de teste

```bash
docker compose --profile tools run --rm aws-cli sqs delete-queue \
  --queue-url http://floci:4566/000000000000/hello-workshop
```

## O que acabou de acontecer?

Você usou comandos do AWS CLI, mas o endpoint foi o Floci rodando no Docker.

Em uma AWS real, o endpoint seria o endpoint oficial do serviço e as credenciais seriam reais.

## Estado final

Ao concluir este laboratório, você deve conseguir responder:

- o que o Floci está simulando;
- por que usamos `localhost:4566`;
- como executar AWS CLI sem instalar AWS CLI localmente;
- como criar, enviar e receber uma mensagem SQS.

O ambiente esperado é:

```text
Seu computador
    |
    +-- Docker
         |
         +-- Floci :4566
```

Nenhuma aplicação do workshop está rodando ainda.

## Checklist de saída

- [ ] Estou na branch `workshop/01-floci`.
- [ ] O container do Floci está ativo.
- [ ] Consigo executar `sqs list-queues`.
- [ ] Consegui enviar e receber uma mensagem manualmente.
- [ ] A fila `hello-workshop` foi removida.

## Pergunta de fixação

**Se o consumer estiver desligado quando a mensagem chega à SQS, a mensagem precisa ser perdida?**

Não. A fila existe justamente para armazenar a mensagem até que um consumidor possa processá-la, respeitando as políticas de retenção configuradas.

## Próximo passo

Vamos introduzir o primeiro componente da aplicação: um producer em Kotlin + Spring Boot.

```bash
git switch workshop/02-producer
```

Continue em [Lab 2 — Publicando o primeiro evento](04-lab-2-producer.md).
