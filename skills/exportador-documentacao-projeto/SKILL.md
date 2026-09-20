---
name: exportador-documentacao-projeto
description: Use esta skill para gerar documentação técnica e funcional completa de projetos Progress OpenEdge e TOTVS Datasul em Markdown estruturado, página HTML interativa independente com busca ao vivo ou layout preparado para exportação em PDF. Mapeia procedures, funções, temp-tables, parâmetros e acessos a banco de dados.
modelInvocable: true
---

# Exportador de Documentação Completa (HTML / Markdown / PDF)

Esta skill realiza a leitura analítica e a documentação completa de projetos e bases de código Progress ABL / OpenEdge / Datasul, gerando especificações técnicas e funcionais detalhadas em três formatos modernos: **Markdown**, **HTML Interativo** e **PDF**.

---

## 1. O que é Extraído dos Fontes Progress?

Para cada programa (`.p`, `.w`, `.cls`, `.i`), a skill analisa e cataloga:
1. **Cabeçalho:** Autor, data, objetivo de negócio, histórico de alterações.
2. **Parâmetros:** Parâmetros de entrada (`INPUT`), saída (`OUTPUT`) e entrada/saída (`INPUT-OUTPUT`).
3. **Temp-Tables e Datasets:** Estrutura completa de tabelas em memória, campos e tipos.
4. **Procedures e Funções Internas:** Nome, objetivo, parâmetros e retorno.
5. **Acesso ao Banco de Dados:** Tabelas consultadas (`FIND`, `FOR EACH`) e modificadas (`CREATE`, `ASSIGN`, `DELETE`).
6. **Pontos de Entrada / EPCs / UPCs:** Chamadas a eventos e extensões.
7. **Includes Utilizados:** Lista de dependências de inclusão.

---

## 2. Formatos de Exportação

### Formato 1: Documentação em Markdown Estruturado
Gera uma pasta `docs/` contendo:
- `INDEX.md`: Sumário geral com tabela de todos os programas, status e módulos.
- `modulos/[modulo]/[programa].md`: Ficha técnica detalhada de cada programa.

Exemplo de Ficha Técnica em Markdown:
```markdown
# [cd0401.p] Manutenção de Itens

> Módulo: Cadastros Gerais (CDP) | Tipo: Procedure ABL

## Objetivo
Realiza a manutenção, validação e atualização cadastral dos itens no ERP Datasul.

## Parâmetros de Entrada / Saída
| Parâmetro | Tipo de Passagem | Tipo de Dado | Descrição |
|---|---|---|---|
| `p-cod-item` | INPUT | CHARACTER | Código do item a ser consultado |
| `p-ok` | OUTPUT | LOGICAL | Retorna TRUE se a operação teve sucesso |
| `TABLE tt-item` | INPUT-OUTPUT | TEMP-TABLE | Registro com dados detalhados |

## Tabelas do Banco de Dados Manipuladas
- `item` (Leitura / Gravação)
- `item-uni-estab` (Leitura)
- `estabelec` (Leitura)
```

---

### Formato 2: HTML Interativo Independente (Single-File)
Gera um arquivo `documentacao.html` autônomo (não necessita de servidor web ou dependências externas), contendo:
- Sidebar com busca instantânea em JavaScript puro.
- Filtro por módulo, nome de programa ou tabela do banco.
- Bloco de visualização com formatação de código limpa e responsiva.
- Modo escuro / claro automático.

Template de estrutura HTML gerada:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Documentação Técnica do Projeto</title>
  <style>
    :root { --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --accent: #38bdf8; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; display: flex; height: 100vh; background: var(--bg); color: var(--text); }
    .sidebar { width: 320px; border-right: 1px solid #334155; padding: 20px; overflow-y: auto; }
    .content { flex: 1; padding: 40px; overflow-y: auto; }
    .search-box { width: 100%; padding: 8px 12px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; margin-bottom: 16px; box-sizing: border-box; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th, td { padding: 10px; border: 1px solid #334155; text-align: left; }
    th { background: #1e293b; color: var(--accent); }
  </style>
</head>
<body>
  <div class="sidebar">
    <h2>Documentação</h2>
    <input type="text" class="search-box" placeholder="Buscar programa..." oninput="filtrar(this.value)">
    <div id="lista-programas"></div>
  </div>
  <div class="content" id="conteudo-principal">
    <!-- Conteúdo do programa selecionado -->
  </div>
</body>
</html>
```

---

### Formato 3: Exportação em PDF
O HTML gerado é estilizado com regras `@media print` otimizadas para PDF:
- Quebras de página automáticas (`page-break-before: always`) antes de cada programa.
- Cabeçalhos e rodapés com numeração de páginas.
- Tipografia ajustada para leitura executiva e técnica.
- Para gerar o PDF, abra o arquivo `documentacao.html` no navegador ou use a ferramenta `Browser` do Progress Code e acione a impressão em PDF.
