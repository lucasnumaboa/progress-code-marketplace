---
name: gerar-changelog
description: Gera ou atualiza o CHANGELOG.md do projeto a partir do histórico do git (commits desde a última tag ou desde uma data), agrupando por tipo (novidades, correções, melhorias) em português. Use quando o usuário pedir changelog, notas de versão, release notes ou "o que mudou".
argument-hint: [tag-ou-data-inicial] [versão]
---

# Gerar changelog

Skill simples, só instruções: o agente usa o git do próprio projeto.

## Passos

1. Descubra o ponto de partida:
   - Se o usuário passou `$1`, use como início (`v1.2.0`, `2026-08-01`, hash).
   - Senão, tente a última tag: `git describe --tags --abbrev=0`. Sem tag, use os últimos 30 dias.
2. Liste os commits: `git log <inicio>..HEAD --pretty=format:"%h|%ad|%an|%s" --date=short --no-merges`.
3. Classifique cada commit pelo texto (prefixo ou palavras):
   - **Novidades**: feat, add, novo, cria, implementa
   - **Correções**: fix, bug, corrige, ajusta, erro
   - **Melhorias**: refactor, perf, melhora, otimiza, chore, docs, build
4. Escreva em `CHANGELOG.md` (crie se não existir; se existir, insira o bloco novo no topo, abaixo do título):

```
## [<versão ou "Não lançado">] - <AAAA-MM-DD>

### Novidades
- Descrição em uma frase, sem o hash (ex.: "Painel lateral para abrir arquivos citados no chat")

### Correções
- …

### Melhorias
- …
```

5. Reescreva as mensagens em linguagem de usuário (o que mudou para quem usa), não em jargão de commit. Junte commits repetidos do mesmo assunto em um item só.
6. Mostre o bloco gerado na resposta e informe quantos commits foram considerados.

## Regras

- Nunca invente mudanças: só o que está no `git log`.
- Não altere tags nem faça commit/push; só grava o arquivo. Se o usuário quiser, ele pede o commit depois.
- Versão (`$2`) vazia → use "Não lançado".
