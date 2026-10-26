# Fundamentos de arquitetura orientada a eventos

## 1. Síncrono x assíncrono

### Síncrono

```text
Cliente -> Serviço A -> Serviço B -> resposta
```

O Serviço A espera o Serviço B terminar.

Vantagens:

- Fácil de entender.
- Resposta imediata.
- Bom para consultas e operações que realmente dependem da resposta.

Custos:

- A latência se soma.
- Uma falha pode se propagar.
- A disponibilidade de A passa a depender de B.

### Assíncrono

```text
Producer -> Evento -> Broker/Fila -> Consumer
```

O producer registra ou publica o que aconteceu e não precisa esperar todos os consumidores terminarem.

---

## 2. O que é um evento?

Um evento representa um fato ocorrido no passado.

Bons nomes:

- `OrderCreated`
- `PaymentApproved`
- `CustomerRegistered`

Evite nomes como:

- `CreateOrder`
- `SendEmail`

Os últimos parecem comandos: dizem a alguém o que fazer. Evento comunica algo que aconteceu.

Exemplo usado no workshop:

```json
{
  "eventId": "a-uuid",
  "orderId": "another-uuid",
  "customerEmail": "dev@aws.local",
  "total": 149.90,
  "occurredAt": "2026-10-26T12:00:00Z"
}
```

---

## 3. Producer

É quem publica o evento.

Neste workshop:

```text
Order API -> OrderCreated
```

A API não chama diretamente notification ou analytics.

Isso reduz acoplamento.

---

## 4. SNS

O Amazon SNS é usado aqui como tópico de publicação.

```text
                 -> subscription A
Producer -> SNS
                 -> subscription B
```

Uma mensagem publicada no tópico pode ser entregue para vários assinantes.

Esse padrão é chamado de **fan-out**.

---

## 5. SQS

Amazon SQS é uma fila de mensagens.

```text
Producer -> Queue -> Consumer
```

A fila desacopla a velocidade de quem produz da velocidade de quem consome.

Se o consumer ficar indisponível, a mensagem pode continuar armazenada na fila para ser processada depois.

---

## 6. Por que usar SNS + SQS juntos?

Queremos que vários consumidores recebam uma cópia independente do mesmo evento.

```text
                    -> notification-queue -> notification worker
Order API -> SNS
                    -> analytics-queue    -> analytics worker
```

Se usássemos apenas uma fila com dois workers diferentes competindo por mensagens, cada mensagem tenderia a ser processada por apenas um deles.

Com SNS + uma fila por consumidor lógico, cada fluxo recebe sua própria cópia.

---

## 7. Visibility Timeout

Quando um consumer recebe uma mensagem da SQS, ela não é imediatamente apagada.

Ela fica temporariamente invisível para outros consumers.

Se o processamento concluir:

```text
receive -> process -> delete
```

Se o processamento falhar e a aplicação não apagar a mensagem:

```text
receive -> failure -> visibility timeout -> message visible again
```

Isso permite retry.

---

## 8. At-least-once e idempotência

Uma mensagem pode ser entregue mais de uma vez.

Por isso, consumidores reais devem ser preparados para receber eventos duplicados sem gerar efeitos duplicados indevidos.

Exemplo clássico:

```text
PaymentApproved recebido duas vezes
```

Não queremos cobrar duas vezes.

O workshop não implementa uma estratégia completa de idempotência porque o foco é a primeira arquitetura orientada a eventos. O tema aparece como desafio final.

---

## 9. Dead Letter Queue

Depois de várias falhas, continuar tentando indefinidamente pode ser ruim.

Uma DLQ recebe mensagens que excederam o limite de tentativas.

```text
main queue -> retry -> retry -> retry -> DLQ
```

A DLQ permite investigar, corrigir e reprocessar posteriormente.

---

## 10. Modelo mental final

```text
Evento = algo aconteceu
Producer = quem comunica
SNS = distribui
SQS = armazena/desacopla
Consumer = reage
DLQ = isola falhas persistentes
```

Se o participante sair do workshop entendendo esses seis conceitos, o objetivo foi atingido.
