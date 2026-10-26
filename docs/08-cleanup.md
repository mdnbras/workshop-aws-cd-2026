# Cleanup e próximos passos

## Parar o laboratório

```bash
docker compose down
```

Isso remove os containers e a rede, mas mantém o volume de dados do Floci.

## Apagar tudo e recomeçar do zero

```bash
docker compose down -v --remove-orphans
```

Depois:

```bash
docker compose up --build -d
```

## Conferir o estado

```bash
docker compose ps
```

## Conceitos que você deve conseguir explicar agora

Sem olhar a documentação, tente responder:

1. O que é um evento?
2. Qual é a responsabilidade do producer?
3. Qual é a diferença entre SNS e SQS neste laboratório?
4. Por que existe uma fila por consumidor lógico?
5. O que acontece quando um consumer recebe uma mensagem e falha antes de apagá-la?
6. Para que serve uma DLQ?
7. Por que consumidores devem ser idempotentes?

## Arquitetura construída

```text
POST /orders
    |
    v
Order API
    |
    | OrderCreated
    v
Amazon SNS (local)
    |
    +-----------------------+
    |                       |
    v                       v
notification-queue      analytics-queue
    |                       |
    v                       v
notification-worker     analytics-worker
    |
    | falha persistente
    v
notification-dlq
```

## Como isso muda na AWS real?

A lógica do AWS SDK continua muito parecida. As maiores mudanças estão ao redor da aplicação:

- endpoint local deixa de ser necessário;
- credenciais dummy deixam de existir;
- use IAM Role em vez de access keys fixas;
- configure policies entre SNS e SQS;
- habilite criptografia quando necessário;
- configure métricas e alarmes;
- decida onde executar as aplicações;
- crie a infraestrutura via IaC;
- pense em custo, quotas e disponibilidade.

## Trilha sugerida de estudo

Depois deste workshop:

1. SQS Standard x FIFO.
2. SNS filter policies.
3. EventBridge.
4. Lambda consumindo eventos.
5. Idempotência.
6. Transactional Outbox.
7. Saga e consistência eventual.
8. Observabilidade com CloudWatch/OpenTelemetry.
9. Infrastructure as Code.

## Regra mais importante

Não escolha event-driven porque está na moda.

Escolha comunicação assíncrona quando o desacoplamento temporal, o isolamento de falhas, o fan-out ou o processamento independente realmente agregarem valor ao sistema.
