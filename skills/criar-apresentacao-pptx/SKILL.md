---
name: criar-apresentacao-pptx
description: Cria apresentações PowerPoint (.pptx) de verdade a partir de um roteiro em JSON: capa, slides de tópicos, tabelas, imagens, duas colunas, citação, notas do apresentador e tema de cores. Use quando o usuário pedir uma apresentação, slides, deck, pitch, treinamento ou resumo em PowerPoint.
argument-hint: <tema ou caminho do roteiro.json> [saida.pptx]
---

# Criar apresentação PowerPoint

Esta skill dá ao agente a capacidade de gerar `.pptx` sem abrir o PowerPoint. O trabalho do modelo é **escrever o roteiro** (JSON) com bom conteúdo; o script `criar_pptx.py` monta o arquivo com layout consistente.

Arquivos desta skill (pasta indicada no cabeçalho): `criar_pptx.py`, `exemplo.json`.
Requisito: Python 3.9+ — o script instala `python-pptx` sozinho na primeira vez (`pip install --user python-pptx`).

## Procedimento

1. **Entenda o pedido**: público, objetivo, quantidade de slides (padrão 8 a 12), tom. Se o usuário anexou um documento (Word, PDF, planilha), extraia o conteúdo com ReadDocument antes de escrever.
2. **Escreva o roteiro** em `docs/apresentacao-<tema>.json` (use Write). Formato:

```json
{
  "titulo": "Título da apresentação",
  "subtitulo": "Subtítulo · autor · data",
  "tema": "azul",
  "rodape": "QualiIT · Confidencial",
  "slides": [
    { "tipo": "secao", "titulo": "Contexto" },
    { "tipo": "topicos", "titulo": "Situação atual", "itens": ["Ponto 1", "Ponto 2", ["Subitem a", "Subitem b"], "Ponto 3"], "notas": "O que falar neste slide" },
    { "tipo": "duas_colunas", "titulo": "Antes × Depois", "esquerda": { "titulo": "Antes", "itens": ["…"] }, "direita": { "titulo": "Depois", "itens": ["…"] } },
    { "tipo": "tabela", "titulo": "Cronograma", "colunas": ["Fase", "Início", "Fim", "Responsável"], "linhas": [["Análise", "01/10", "10/10", "Lucas"], ["Desenvolvimento", "11/10", "30/10", "Matheus"]] },
    { "tipo": "imagem", "titulo": "Tela atual", "caminho": "docs/tela.png", "legenda": "Programa cd0704" },
    { "tipo": "citacao", "texto": "Frase de impacto ou depoimento", "autor": "Cliente X" },
    { "tipo": "numeros", "titulo": "Resultados", "itens": [{ "valor": "38%", "rotulo": "menos retrabalho" }, { "valor": "R$ 120 mil", "rotulo": "economia/ano" }, { "valor": "5 dias", "rotulo": "de implantação" }] },
    { "tipo": "encerramento", "titulo": "Próximos passos", "itens": ["Aprovar escopo", "Kick-off dia 15"], "contato": "lucas.oliveira@qualiit.com.br" }
  ]
}
```

   Temas disponíveis: `azul` (padrão), `roxo`, `verde`, `grafite`, `laranja`. Tipos: `capa` (automático a partir de titulo/subtitulo), `secao`, `topicos`, `duas_colunas`, `tabela`, `imagem`, `citacao`, `numeros`, `encerramento`.

3. **Gere o arquivo**:
   `python "<pasta-da-skill>/criar_pptx.py" docs/apresentacao-<tema>.json saida/<nome>.pptx`
   O script imprime o caminho final e o número de slides. Erros de formato vêm com a linha do JSON.
4. **Confira e entregue**: use `ReadDocument(file_path="saida/<nome>.pptx")` para revisar o texto de cada slide; corrija o JSON e gere de novo se precisar. Na resposta, cite o caminho do `.pptx` e do roteiro.

## Boas práticas de conteúdo

- Um assunto por slide; até 6 tópicos, frases curtas (máx. ~12 palavras), verbos de ação.
- Capa + agenda/seção + conteúdo + números/resultados + encerramento com próximos passos.
- Tabelas com até 6 colunas e 8 linhas; mais que isso, divida em dois slides.
- Use `notas` para o roteiro de fala; não repita o texto do slide.
- Imagens: só caminhos que existem (verifique com ListDir); PNG/JPG. Sem imagem disponível, prefira `numeros` ou `duas_colunas`.
- Não invente dados: números vêm do usuário ou dos documentos anexados; marque "a confirmar" quando estimados.
