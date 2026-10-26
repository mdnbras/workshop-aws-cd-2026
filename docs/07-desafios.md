# Desafios extras

Use estes exercícios se a turma avançar rápido ou como material pós-workshop.

## Desafio 1 — Novo consumidor sem alterar o producer

Objetivo: provar o desacoplamento.

Crie:

```text
fraud-queue
```

Assine essa fila no mesmo `orders-topic` e execute uma terceira instância do `event-worker` com:

```text
WORKER_NAME=fraud
```

Pergunta: foi necessário alterar a `Order API`?

Resposta esperada: não.

---

## Desafio 2 — Filtro no SNS

Adicione um atributo de mensagem, por exemplo:

```text
orderType=PREMIUM
```

Configure uma subscription para receber apenas eventos de determinado tipo.

Pesquise o conceito de **SNS subscription filter policy**.

---

## Desafio 3 — Idempotência

Hoje um evento entregue duas vezes produziria dois efeitos no worker.

Implemente um armazenamento de `eventId` já processados.

Antes de executar:

```text
if eventId already processed -> ignore
else -> process and save eventId
```

Em uma AWS real, DynamoDB é uma opção comum para esse tipo de controle dependendo do contexto.

---

## Desafio 4 — Contrato versionado

Adicione ao evento:

```json
{
  "eventVersion": 1
}
```

Depois evolua para versão 2 adicionando um campo sem quebrar os consumidores antigos.

Discuta:

- campos opcionais;
- compatibilidade retroativa;
- remoção de campos;
- Schema Registry como evolução futura.

---

## Desafio 5 — EventBridge

Refaça a distribuição usando Amazon EventBridge em vez de SNS.

Compare:

- roteamento;
- filtros;
- regras;
- fan-out;
- complexidade.

O objetivo não é concluir que um é sempre melhor. É entender quando cada serviço combina melhor com o problema.

---

## Desafio 6 — Persistência e Outbox

No workshop, o endpoint publica diretamente no SNS.

Em sistemas reais existe um problema clássico:

```text
1. salvar pedido no banco = sucesso
2. publicar evento = falha
```

Pesquise e implemente o **Transactional Outbox Pattern**.

Esse desafio conecta o workshop introdutório com temas mais avançados de sistemas distribuídos.

---

## Desafio 7 — Observabilidade

Adicione:

- correlation ID;
- logs estruturados;
- contador de eventos processados;
- contador de falhas;
- tempo de processamento.

Depois pesquise como esses sinais poderiam ser enviados para CloudWatch e OpenTelemetry em produção.

---

## Desafio 8 — Levar para uma conta AWS real

Mapeie os recursos locais para recursos reais:

| Local | AWS real |
|---|---|
| Floci SNS | Amazon SNS |
| Floci SQS | Amazon SQS |
| Docker worker | ECS/EKS/Lambda/EC2, conforme contexto |
| Docker Order API | ECS/EKS/EC2/Lambda + API Gateway, conforme arquitetura |

Antes de executar em uma conta real, adicione:

- IAM least privilege;
- criptografia;
- networking;
- CloudWatch;
- alarmes de DLQ;
- IaC com Terraform/CDK/CloudFormation;
- tags e orçamento.
