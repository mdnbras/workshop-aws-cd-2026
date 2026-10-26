# Apresentação HTML do workshop

A apresentação principal está em [`index.html`](index.html).

## Como abrir

Você pode abrir o arquivo diretamente no navegador ou servir a pasta com qualquer servidor HTTP local.

Exemplo com Python:

```bash
cd presentation
python -m http.server 8088
```

Depois acesse `http://localhost:8088`.

## Controles

- `→`, `PageDown` ou `Espaço`: próximo slide
- `←` ou `PageUp`: slide anterior
- `Home`: primeiro slide
- `End`: último slide
- `F`: tela cheia
- `N`: notas do apresentador
- `M`: visão geral dos slides
- Swipe lateral também funciona em telas touch

## Características

- HTML, CSS e JavaScript em um único arquivo
- Sem bibliotecas ou CDN externas
- Funciona offline depois do clone
- Layout responsivo
- Transições entre slides
- Barra de progresso
- Menu de navegação
- Notas do apresentador
- Preparado para impressão/exportação pelo navegador

O deck acompanha as mesmas cinco branches do workshop: `workshop/01-floci`, `workshop/02-producer`, `workshop/03-fanout`, `workshop/04-consumers` e `workshop/05-dlq-final`.
