# Catálogo do Progress Code (marketplace)

Publique este diretório como um repositório público no GitHub (ex.: `lucasnumaboa/progress-code-marketplace`, branch `main`).
No app: Configurações → Marketplace → Adicionar fonte → `https://github.com/lucasnumaboa/progress-code-marketplace`.

## index.json

```json
{ "name": "Nome do catálogo", "description": "opcional",
  "items": [ { "id": "unico", "type": "skill|agent|command|mcp|team|pack", "name": "…", "description": "…",
               "version": "1.0.0", "author": "…", "tags": ["…"], "url": "skills/x.zip", "homepage": "https://…" } ] }
```

- `url` pode ser relativa ao index.json (fica dentro do repositório) ou absoluta.
- **skill**: `SKILL.md` ou `.zip` com a pasta da skill (SKILL.md + scripts). Instala em `%APPDATA%\Progress Code\skills\<nome>`.
- **agent** / **command**: arquivo `.md` com frontmatter. Vão para `agents\` e `commands\` do app.
- **mcp**: `.json` com `{ "mcpServers": { "nome": { "type": "stdio", "command": "…", "args": [] } } }` (ou `config` inline no index). Entra em Configurações → Servidores MCP.
- **team**: `.json` com `{ "teams": [ … ] }` no formato de `settings.json`. Entra em Configurações → Multiagente.
- **pack**: `.zip` com pastas `skills/`, `agents/`, `commands/` e arquivos `mcp.json`, `teams.json` — instala tudo de uma vez.
- `version` diferente da instalada mostra o botão **Atualizar**. Só .zip (não .rar): o app extrai sem programa externo.

Nunca coloque chaves de API nos arquivos: as skills devem ler variáveis de ambiente ou um `apikey.txt` local.
