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

## Skills de especialistas usadas pelos bots (2.0)

Os bots 2.0 vêm com skills de especialistas publicadas com licença aberta. Cada zip em `skills/` traz o texto original (em inglês), o arquivo de licença e um NOTICE.md com a origem, o commit e as mudanças feitas (só remoção de telemetria, propaganda e instruções presas a outros produtos, e o `name` do frontmatter). Elas ficam fora do catálogo geral de skills (`botOnly`) e são baixadas só para a pasta do bot.

| Repositório | Autor e licença | Skills |
|---|---|---|
| https://github.com/anthropics/claude-cookbooks | Anthropic (MIT) | 4: acb-agent-patterns, acb-citations-agent, acb-research-lead-agent, acb-research-subagent |
| https://github.com/addyosmani/web-quality-skills | Addy Osmani (MIT) | 3: addy-accessibility, addy-core-web-vitals, addy-web-quality-audit |
| https://github.com/brendanlong/alt-text-skill | Brendan Long (MIT) | 1: alt-alt-text |
| https://github.com/anthropics/skills | Anthropic (Apache-2.0) | 4: as-mcp-builder, as-pptx, as-skill-creator, as-webapp-testing |
| https://github.com/TheCraigHewitt/skills | Craig Hewitt (MIT) | 16: ch-call-debrief, ch-cold-call, ch-deep-research, ch-discovery-call, ch-forecast, ch-hook-writing, ch-inbox-triage, ch-meeting-prep, ch-morning-briefing, ch-negotiation, ch-objection-handling, ch-outbound-sequence, ch-referral-intro, ch-retention-editing, ch-script-structure, ch-thumbnail-design |
| https://github.com/obra/the-elements-of-style | William Strunk Jr. (texto de 1918) e Jesse Vincent (empacotamento) (Domínio público) | 1: eos-writing-clearly-and-concisely |
| https://github.com/ericosiu/ai-marketing-skills | Single Grain (MIT) | 4: es-commenter-talent-scan, es-packaging-youtube-thumbnails, es-shortform-production, es-video-clip-pipeline |
| https://github.com/growthenginenowoslawski/coldoutboundskills | GrowthEngineX (MIT) | 8: gex-campaign-copywriting, gex-campaign-strategy, gex-cold-email-weekly-rhythm, gex-list-quality-scorecard, gex-perfect-company-list, gex-playbook-hiring-surge, gex-playbook-job-posting-language, gex-playbook-warm-intros |
| https://github.com/garrytan/gstack | Garry Tan (MIT) | 1: gs-office-hours |
| https://github.com/blader/humanizer | Siqi Chen (MIT) | 1: hum-humanizer |
| https://github.com/pbakaus/impeccable | Paul Bakaus (Apache-2.0) | 2: imp-document, imp-extract |
| https://github.com/anthropics/knowledge-work-plugins | Anthropic (Apache-2.0) | 47: kwp-account-plan, kwp-account-research, kwp-account-tiering, kwp-call-prep, kwp-call-summary, kwp-campaign-plan, kwp-competitive-brief, kwp-create-an-asset, kwp-crm-hygiene-check, kwp-customer-health, kwp-customer-voice, kwp-deal-advance-gap, kwp-deal-review, kwp-deal-slip-scenario, kwp-deploy-checklist, kwp-design-critique, kwp-design-handoff, kwp-design-system, kwp-digest, kwp-draft-outreach, kwp-draft-response, kwp-end-of-day, kwp-forecast, kwp-handle-objection, kwp-inbox-sweep, kwp-incident-response, kwp-kb-article, kwp-knowledge-synthesis, kwp-lead-triage, kwp-log-activity, kwp-performance-report, kwp-pipeline-review, kwp-pm-competitive-brief, kwp-process-doc, kwp-renewal-radar, kwp-review-contract, kwp-route-lead, kwp-runbook, kwp-seo-ai-visibility, kwp-speed-to-lead, kwp-sprint-planning, kwp-stakeholder-map, kwp-status-report, kwp-task-management, kwp-update-opportunity, kwp-vendor-review, kwp-write-spec |
| https://github.com/mvanhorn/last30days-skill | Matt Van Horn (MIT) | 1: l30-last30days |
| https://github.com/coreyhaines31/marketingskills | Corey Haines (MIT) | 28: mk-ab-testing, mk-ad-creative, mk-ads, mk-ai-seo, mk-analytics, mk-aso, mk-attribution, mk-co-marketing, mk-cold-email, mk-community-marketing, mk-competitor-profiling, mk-content-strategy, mk-copy-editing, mk-copywriting, mk-cro, mk-customer-research, mk-directory-submissions, mk-events, mk-launch, mk-marketing-plan, mk-pricing, mk-product-marketing, mk-prospecting, mk-reverse-engineer-marketing, mk-revops, mk-seo-audit, mk-social, mk-video |
| https://github.com/mattpocock/skills | Matt Pocock (MIT) | 4: mp-diagnosing-bugs, mp-prototype, mp-to-tickets, mp-writing-for-agents |
| https://github.com/phuryn/pm-skills | Paweł Huryn (The Product Compass) (MIT) | 9: ph-brainstorm-experiments-new, ph-competitor-analysis, ph-create-prd, ph-identify-assumptions-new, ph-positioning-ideas, ph-pre-mortem, ph-prioritization-frameworks, ph-strategy-red-team, ph-value-prop-statements |
| https://github.com/getsentry/skills | Sentry (Apache-2.0) | 7: sen-blog-writing-guide, sen-code-review, sen-find-bugs, sen-iterate-pr, sen-pr-writer, sen-prompt-optimizer, sen-skill-writer |
| https://github.com/shawnpang/startup-founder-skills | Shawn Pang (MIT) | 6: sfs-competitor-monitoring, sfs-daily-product-digest, sfs-event-hosting, sfs-investor-research, sfs-pitch-deck, sfs-sourcing-outreach |
| https://github.com/hardikpandya/stop-slop | Hardik Pandya (MIT) | 1: slop-stop-slop |
| https://github.com/Sloydai/game-art-skills | Sloyd (MIT) | 1: sloyd-art-director |
| https://github.com/obra/superpowers | Jesse Vincent (MIT) | 10: sp-dispatching-parallel-agents, sp-finishing-a-development-branch, sp-receiving-code-review, sp-requesting-code-review, sp-subagent-driven-development, sp-systematic-debugging, sp-test-driven-development, sp-verification-before-completion, sp-writing-plans, sp-writing-skills |
| https://github.com/swan-gtm/gtm-skills | Ivan Falco (MIT) | 41: swan-ads-budget-allocation, swan-ads-measurement-scorecard, swan-ads-optimization-signals, swan-b2b-case-study-production, swan-buying-signals-6, swan-call-followup-sweep, swan-call-scorecards, swan-cold-email-4-sequence, swan-competitor-monitoring, swan-conference-meeting-cards, swan-creative-fatigue-detection, swan-deal-qualification-gates, swan-event-room-intelligence, swan-evidence-based-call-scoring, swan-expansion-revenue-architect, swan-hiring-intake-brief, swan-hiring-radar, swan-hiring-scorecard, swan-hiring-signal-prospecting, swan-hiring-signal-verification, swan-icp-builder, swan-inbound-is-data, swan-message-validation, swan-meta-reporting, swan-multi-threading-coach, swan-panel-debrief-alignment, swan-partner-ecosystem-architect, swan-positioning-messaging-designer, swan-post-event-roi-report, swan-post-meeting-execution, swan-pull-call-review, swan-qbr-ebr-builder, swan-renewal-save-motion, swan-revops-forecasting, swan-roi-proof-generator, swan-seo-topic-research-pipeline, swan-signal-sourcer, swan-signal-timing, swan-stage-aware-follow-up, swan-warm-intro-intelligence, swan-zero-click-organic-pipeline-audit |
| https://github.com/browser-use/video-use | Browser Use (MIT) | 1: vu-video-use |
