# Infraestrutura AWS real com Terraform

Esta pasta é opcional no workshop. O fluxo principal continua usando Docker + Floci.

Use este modo se você quiser executar a mesma arquitetura em uma conta AWS própria.

## Arquitetura provisionada

```text
Order API
   |
   v
SNS topic
   |
   +--> notification-queue --> notification-worker
   |          |
   |          +--> notification-dlq após falhas repetidas
   |
   +--> analytics-queue --> analytics-worker
```

## Recursos criados

- 1 tópico Amazon SNS
- 2 filas Amazon SQS
- 1 Dead Letter Queue
- 2 subscriptions SNS -> SQS
- políticas SQS permitindo `sns.amazonaws.com` enviar mensagens apenas a partir do tópico do workshop
- redrive policy da fila de notificação

## Pré-requisitos

- Terraform >= 1.7
- AWS CLI autenticado ou credenciais AWS exportadas no ambiente
- permissão para criar SNS, SQS e políticas relacionadas

Valide sua identidade antes de aplicar:

```bash
aws sts get-caller-identity
```

## 1. Configure os nomes

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
```

No Windows PowerShell:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Edite `terraform.tfvars` e use um prefixo próprio:

```hcl
aws_region  = "us-east-1"
name_prefix = "workshop-eda-seu-nome"
```

## 2. Inicialize

```bash
terraform init
terraform fmt
terraform validate
```

## 3. Revise o plano

```bash
terraform plan
```

Leia o plano antes de continuar. Terraform mostrará os recursos que serão criados na sua conta AWS.

## 4. Provisione

```bash
terraform apply
```

Confirme digitando `yes` quando solicitado.

Depois:

```bash
terraform output
```

Você verá o ARN do tópico SNS e as URLs das filas SQS.

## 5. Gere o arquivo de configuração das aplicações

Linux/macOS/Git Bash:

```bash
./generate-env.sh
```

Windows PowerShell:

```powershell
./generate-env.ps1
```

O arquivo `.env.aws` será criado na raiz do projeto com:

```text
AWS_REGION=...
ORDERS_TOPIC_ARN=...
NOTIFICATION_QUEUE_URL=...
ANALYTICS_QUEUE_URL=...
```

Credenciais AWS não são gravadas no arquivo.

## 6. Exporte as credenciais para os containers

Se você usa access keys temporárias ou credenciais de laboratório, exporte as variáveis fornecidas pelo seu ambiente.

Linux/macOS/Git Bash:

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."   # quando existir
```

PowerShell:

```powershell
$env:AWS_ACCESS_KEY_ID="..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_SESSION_TOKEN="..."     # quando existir
```

Não faça commit dessas credenciais.

## 7. Execute as aplicações contra a AWS real

Volte para a raiz do projeto:

```bash
cd ../..
```

Suba usando o compose dedicado à AWS real:

```bash
docker compose --env-file .env.aws -f compose.aws.yaml up --build
```

O arquivo `compose.aws.yaml` não inicia Floci e não define `AWS_ENDPOINT_URL`. Por isso o AWS SDK usa os endpoints oficiais da AWS.

## 8. Publique um evento

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"dev@aws.local","total":149.90}'
```

Acompanhe:

```bash
docker compose --env-file .env.aws -f compose.aws.yaml logs -f
```

## 9. Demonstre a DLQ

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerEmail":"fail@workshop.local","total":99.90}'
```

O `notification-worker` falha propositalmente. Após o limite de recebimentos definido no Terraform, o SQS move a mensagem para a DLQ.

Consulte a DLQ usando a URL retornada por:

```bash
cd infra/terraform
terraform output -raw notification_dlq_url
```

Depois:

```bash
aws sqs receive-message \
  --region us-east-1 \
  --queue-url "COLE_A_URL_DA_DLQ"
```

## 10. Destrua os recursos

Ao terminar, execute obrigatoriamente:

```bash
terraform destroy
```

Confirme com `yes`.

Verifique no console AWS ou com CLI se os recursos do prefixo escolhido foram removidos.

## Custos

SNS e SQS possuem cobrança por uso e podem estar cobertos parcialmente por níveis gratuitos/promocionais dependendo da conta e do momento. Não assuma custo zero em uma conta real.

O workshop mantém volume mínimo, mas cada participante é responsável pelos recursos criados em sua conta.

Sempre execute `terraform destroy` ao final.

## Segurança

Para aprendizado, é comum o participante usar credenciais temporárias de laboratório ou uma identidade com permissões amplas. Em ambientes reais, use menor privilégio.

A aplicação precisa, no mínimo, de:

- `sns:Publish` no tópico de pedidos
- `sqs:ReceiveMessage`
- `sqs:DeleteMessage`
- `sqs:GetQueueAttributes`
- `sqs:ChangeMessageVisibility`

nas filas consumidas.

O Terraform precisa de permissões adicionais para criar e remover os recursos.

## Floci x AWS real

| Item | Floci | AWS real |
|---|---|---|
| Conta AWS | não | sim |
| Billing | não | possível |
| Endpoint | `floci:4566` | endpoints AWS |
| Credenciais | fictícias | reais/temporárias |
| Terraform | opcional | recomendado |
| Cleanup | `docker compose down -v` | `terraform destroy` |
