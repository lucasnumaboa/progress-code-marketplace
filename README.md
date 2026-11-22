# Catálogo do Progress Code (marketplace)

Publique este diretório como um repositório público no GitHub (ex.: `lucasnumaboa/progress-code-marketplace`, branch `main`).
No app: Configurações → Marketplace → Adicionar fonte → `https://github.com/lucasnumaboa/progress-code-marketplace`.

## index.json

```json
{ "name": "Nome do catálogo", "description": "opcional",
  "items": [ { "id": "unico", "type": "skill|agent|command|mcp|team|pack|bot", "name": "…", "description": "…",
               "version": "1.0.0", "author": "…", "tags": ["…"], "url": "skills/x.zip", "homepage": "https://…" } ] }
```

- `url` pode ser relativa ao index.json (fica dentro do repositório) ou absoluta.
- **skill**: `SKILL.md` ou `.zip` com a pasta da skill (SKILL.md + scripts). Instala em `%APPDATA%\Progress Code\skills\<nome>`.
- **agent** / **command**: arquivo `.md` com frontmatter. Vão para `agents\` e `commands\` do app.
- **mcp**: `.json` com `{ "mcpServers": { "nome": { "type": "stdio", "command": "…", "args": [] } } }` (ou `config` inline no index). Entra em Configurações → Servidores MCP.
- **team**: `.json` com `{ "teams": [ … ] }` (formato do antigo modo multiagente). Cada papel vira um bot do Prog Bot.
- **bot**: `.json` no formato `progress-code-bot` (template: nome, cargo, instruções, skills, conectores e rotinas) em `bots/<id>.json`, com `category` no index e ícone em `icons/bots/<id>.svg`. Aparece em Personalizar → Marketplace de bots. As skills que o bot usa (ids das skills deste catálogo) são baixadas só para a pasta dele; as rotinas chegam desligadas; contas e chaves nunca vêm no template.
- **pack**: `.zip` com pastas `skills/`, `agents/`, `commands/` e arquivos `mcp.json`, `teams.json` — instala tudo de uma vez.
- `version` diferente da instalada mostra o botão **Atualizar**. Só .zip (não .rar): o app extrai sem programa externo.

Nunca coloque chaves de API nos arquivos: as skills devem ler variáveis de ambiente ou um `apikey.txt` local.

## Créditos e licenças de terceiros

- `skills/frontend-design.zip`: skill "frontend-design" da Anthropic (https://github.com/anthropics/skills), Apache-2.0, sem alterações; licença dentro do zip.
- `skills/site-com-cara-propria.zip` (2.0.0 em diante): obra derivada (tradução, resumo e reorganização) de Impeccable, de Paul Bakaus (https://github.com/pbakaus/impeccable), e de frontend-design, da Anthropic, ambas Apache-2.0; licenças e NOTICE dentro do zip.
