# Pré-requisitos do participante

O workshop foi desenhado para reduzir ao máximo problemas de setup.

## Obrigatório

- Git
- Docker 20.10+
- Docker Compose v2+
- curl, Postman ou Insomnia
- Editor de código de sua preferência

## Não é obrigatório instalar

- Java
- Maven
- AWS CLI
- Conta AWS

O build do Java/Maven e o AWS CLI são executados em containers.

## Verificação antes do evento

```bash
git --version
docker --version
docker compose version
```

Clone o repositório:

```bash
git clone https://github.com/mdnbras/workshop-aws-cd-2026.git
cd workshop-aws-cd-2026
```

Baixe previamente as imagens para evitar depender do Wi-Fi do evento:

```bash
docker compose pull
docker compose build
```

## Portas utilizadas

| Porta | Uso |
|---|---|
| 4566 | Floci / APIs AWS locais |
| 8080 | Order API |

Verifique se não há outro processo usando essas portas.

## Windows

Recomendado:

- Docker Desktop atualizado.
- Executar comandos no PowerShell, Windows Terminal ou WSL2.
- Usar `docker compose` e não o antigo comando `docker-compose`.

## Teste rápido

```bash
docker compose up floci
```

Em outro terminal:

```bash
curl http://localhost:4566
```

Uma resposta HTTP do Floci já confirma que a porta está acessível. Pare o teste com `Ctrl+C`.

## Checklist do instrutor

Antes de começar:

- [ ] Repositório clonado.
- [ ] Imagens Docker baixadas.
- [ ] Build concluído ao menos uma vez.
- [ ] Portas 4566 e 8080 livres.
- [ ] Exemplo de curl pronto para copiar.
- [ ] Terminal com fonte grande para projeção.
