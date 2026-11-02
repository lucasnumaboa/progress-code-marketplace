---
name: produtos-personalizados-3d
description: Gera produtos personalizados para impressão 3D (tigela de pet com nome, plaquinha de coleira com nome) a partir de receitas paramétricas do SolidCraft, exporta 3MF/STL/STEP com prévia em imagem, fatia na Bambu Lab A1 e calcula custo e preço de venda na Shopee. Use quando pedirem uma peça com nome, uma tigela/comedouro personalizado, plaquinha de pet, orçamento de peça impressa ou um estilo novo de produto personalizado.
argument-hint: <produto> --nome <Nome> [--estilo lisa|canelada] [--diametro 140] ...
---

# Produtos personalizados 3D

Fica em cima do **3D Maker** do Progress Code (SolidCraft). O 3D Maker instala o `solidcraft-cli.exe` em
`%APPDATA%\Progress Code\tools\solidcraft\`; se não houver, peça para o usuário abrir o 3D Maker uma vez.

Os scripts estão na pasta `scripts` desta skill. Rode com `python` (precisa de Pillow: `pip install pillow`).

## Fluxo de um pedido

1. **Entenda o pedido** e escolha o produto e os parâmetros (tabela abaixo). Não invente medida fora dos
   limites: o script recusa e diz o limite.
2. **Gere a peça:**
   ```
   python scripts/gerar.py tigela --nome Thor --estilo lisa --diametro 140 --altura 60
   ```
   Sai em `Documentos\3D Maker\personalizados\<produto>-<estilo>-<nome>\`: `peca.3mf`, `peca.stl`,
   `peca.step`, `previa-iso.png`, `previa-front.png`, `medidas.json` (volume, massa, caixa), `receita.json`.
   Medido neste PC: tigela lisa com nome ~65 s; canelada com nome ~105 s (36 frisos).
3. **Olhe a prévia** (`previa-front.png` mostra o nome de frente) antes de dizer que ficou pronto. Confira
   se o nome está inteiro e legível e se `medidas.json` tem `body_count: 1`.
4. **Orce:**
   ```
   python scripts/orcar.py "<pasta>\peca.3mf" --material PETG --paredes 4
   ```
   Fatia na A1 (Bambu Studio CLI) e devolve horas, gramas, custo, taxa da Shopee, preço sugerido (menor
   ,90 com a margem alvo) e lucro. `--preco 49.90` confere um preço escolhido. `--embalagem 1.5` troca o
   custo de embalagem (plaquinha é bem menor que tigela).
5. **Responda** com a prévia, as medidas, o tempo/peso e o preço. Diga o que é estimativa (veja abaixo).

`python scripts/gerar.py --listar` mostra produtos, padrões, limites e fontes.

## Produtos

| Produto | Parâmetros (padrão) | Observações |
|---|---|---|
| `tigela` | `estilo` lisa\|canelada, `diametro` 140 (80–220), `altura` 60 (35–110), `parede` 4, `fundo` 4, `raio_fundo` 6, `nome`, `fonte`, `altura_letra` 12 (7–20), `saliencia` 1.2 | Parede reta. Nome em relevo em volta da parede, de frente (-Y). Canelada: frisos (`friso` 6 mm, `n_frisos` 36) embaixo e faixa lisa em cima para o nome. |
| `plaquinha` | `diametro` 32 (22–45), `espessura` 3, `furo` 4, `nome`, `fonte`, `altura_letra` 6 (4–9), `saliencia` 0.8 | Redonda, furo para a argola, nome em relevo na frente. |

Fontes: `arredondada` (Arial Rounded MT Bold, padrão), `negrito` (Arial Bold), `divertida` (Comic Sans Bold).

**Tamanho do nome:** nome longo numa tigela pequena dá volta demais. Regra prática: o nome deve ocupar no
máximo ~1/3 da volta (π·diâmetro/3; numa de 140 mm, ~145 mm de texto). Se passar, diminua `altura_letra`.
Na plaquinha, nomes de até ~6 letras com `altura_letra` 6 cabem em 32 mm.

## Impressão e uso

- **Material:** PETG para tigela (aguenta água e lavagem melhor que PLA). Plaquinha: PETG ou PLA.
- **Tigela de água:** use `--paredes 4` ou mais no orçamento e no fatiamento real, para não vazar.
- **Contato com comida:** peça impressa tem frestas entre camadas. Na descrição do produto, indique ração
  seca, lavagem à mão e nada de lava-louças ou água fervente. Não diga que é "atóxico" ou "food safe".
- Imprima a tigela com o fundo na mesa (como gerada), sem suporte.

## Configuração de custos

`%APPDATA%\Progress Code\produtos-personalizados-3d\config.json` (criado no primeiro `orcar.py`): preço do
filamento por kg, potência da impressora, tarifa de energia, perda, embalagem, margem alvo e faixas de taxa
da Shopee. **Os valores iniciais são exemplo** (A1 = 95 W da wiki da Bambu; Enel SP ~R$ 0,95/kWh; taxa
Shopee 2026 de terceiros). Peça ao usuário para confirmar os dele antes de usar o preço em anúncio.

## Criar um produto ou estilo novo

1. Modele e teste primeiro pelo MCP do 3D Maker (skills `solidcraft-modeling` e `solidcraft-checking`).
2. Escreva a receita como função em `scripts/produtos.py` (lista de comandos do SolidCraft, medidas em mm)
   e registre em `PRODUTOS` com padrões e limites.
3. Gere com `gerar.py`, olhe as prévias e confira `body_count: 1`. Atualize a tabela acima.

### Armadilhas do SolidCraft 0.16.2 (comprovadas)

- **Texto em parede curva:** `solid.emboss` em cilindro aceita só retângulos ("only orthogonal line profiles
  are supported on cylinders") e exige o cilindro maciço com duas tampas planas. Use `nome_em_volta()` de
  `produtos.py`: cada letra num plano tangente próprio, extrudada para dentro da parede (folga ~0,2 mm com
  letra de 12 mm em raio 70 mm). Faça as letras **antes** de cavar o miolo.
- **Negrito:** a fonte embutida não tem negrito; passe o caminho de um `.ttf` em `font`.
- `run` sem `--results` com `--json-out` grava as medidas: um recálculo só. `snapshot --in peca.step` gera
  a imagem sem refazer a receita (cada recálculo de uma tigela com nome leva ~20-60 s).
- Bambu Studio CLI: código -17 = processo sem `compatible_printers`; -50 = impressora sem `inherits` ou peça
  fora da mesa; -61 = mesa incompatível com o filamento (`curr_bed_type`). `orcar.py` já trata os três.
