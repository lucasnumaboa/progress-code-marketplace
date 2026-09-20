---
name: extrator-regras-datasul-epc-upc
description: Use esta skill para analisar fontes do TOTVS Datasul (.p, .w, .i), identificar automaticamente todos os pontos de chamada de UPC (User Program Call) e EPC (Enterprise Program Call), mapear eventos, tabelas de parâmetros de entrada/saída e gerar documentação de regras de negócio e esqueletos de customização prontos.
modelInvocable: true
---

# Extrator de Regras de Negócio e Pontos de Entrada (EPC / UPC Datasul)

Esta skill é especializada em fazer engenharia reversa e auditoria de regras de negócio em programas padrão do ERP TOTVS Datasul (EMS 2, EMS 5 e TOTVS 12), localizando todos os pontos de customização disponíveis e documentando a lógica de negócio.

---

## 1. O que são EPCs e UPCs no Datasul?

- **UPC (User Program Call):** Mecanismo clássico onde o programa padrão chama um programa customizado pelo cliente para adicionar ou alterar comportamentos antes, durante ou depois de uma transação (ex.: `esp/upc_cd0401.p`).
- **EPC (Enterprise Program Call):** Mecanismo unificado e baseado em eventos do framework Datasul (`utp/ut-epc.p` ou `utp/ut-api.p`), onde múltiplos módulos e customizações escutam eventos específicos (ex: `BEFORE-COMMIT`, `AFTER-VALIDATE`, `CALCULATE-PRICES`).

---

## 2. Padrões de Busca e Extração nos Fontes

Ao escanear um fonte ou diretório de fontes Progress ABL, procure pelas seguintes assinaturas e padrões:

### Padrão 1: Chamada Direta de UPC
```progress
/* Chamada clássica de UPC por programa específico */
IF CAN-FIND(FIRST programa-upc WHERE programa-upc.cd-programa = "cd0401") THEN DO:
    RUN esp/upc_cd0401.p (INPUT "VALIDA-CAMPOS", INPUT-OUTPUT TABLE tt-item).
END.
```

### Padrão 2: Chamada de Framework EPC (utp/ut-epc.p)
```progress
/* Chamada padrão de ponto de entrada EPC */
RUN utp/ut-epc.p (INPUT "cd0401",
                  INPUT "BEFORE-CREATE",
                  INPUT-OUTPUT TABLE RowErrors,
                  INPUT-OUTPUT TABLE tt-item).
```

### Padrão 3: Include de Chamada Genérica
```progress
{include/i-epc.i &Program="in0101" &Event="AFTER-SAVE"}
```

---

## 3. Como Realizar a Análise Passo a Passo

### Passo 1: Varredura de Fontes
Utilize a ferramenta `Grep` ou scripts de busca para encontrar ocorrências de:
- `ut-epc.p`
- `ut-api.p`
- `upc_`
- `RowErrors`
- `VALIDATE-` ou `BEFORE-` ou `AFTER-`

### Passo 2: Mapeamento de Parâmetros e Temp-Tables
Para cada ponto encontrado, documente:
1. **Nome do Evento:** (Ex: `AFTER-COMMIT`)
2. **Momento de Disparo:** Se ocorre antes do lock da tabela, durante a validação ou após a gravação definitiva.
3. **Parâmetros Trafegados:** Temp-tables com dados originais (`tt-item-orig`) e modificados (`tt-item`).
4. **Controle de Erros:** Como o programa padrão interrompe a execução caso o UPC retorne erro (geralmente inserindo registros na temp-table `RowErrors`).

### Passo 3: Geração do Catálogo de Pontos de Entrada
Exporte a documentação estruturada no seguinte formato Markdown:

```markdown
# Catálogo de Pontos de Entrada: [Nome do Programa]

| Evento EPC | Linha no Fonte | Temp-Tables / Parâmetros | Finalidade de Negócio |
|---|---|---|---|
| `VALIDATE-ITEM` | L412 | `tt-item`, `RowErrors` | Permite validação de atributos fiscais customizados antes de gravar. |
| `AFTER-CREATE` | L580 | `tt-item` | Permite criar registros complementares em tabelas específicas do cliente. |
| `BEFORE-DELETE` | L890 | `tt-item`, `RowErrors` | Impede exclusão se houver movimentações em sistemas legados. |
```

---

## 4. Geração de Template de UPC Customizado

Gere o esqueleto do programa customizado do cliente pronto para compilação, com segurança de transação e isolamento de erros:

```progress
/********************************************************************************
** Programa: esp/upc_[programa].p
** Objetivo: Customização de regras de negócio via UPC Datasul
********************************************************************************/
{utp/ut-glob.i}

DEFINE INPUT        PARAMETER p-event  AS CHARACTER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR RowErrors.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tt-registro.

CASE p-event:
    WHEN "BEFORE-CREATE" THEN DO:
        /* Regra customizada antes de criar */
    END.
    WHEN "VALIDATE-FIELDS" THEN DO:
        /* Validações customizadas. Para abortar com erro: */
        /*
        CREATE RowErrors.
        ASSIGN RowErrors.ErrorNumber   = 99999
               RowErrors.ErrorText     = "Regra violada: preenchimento obrigatório do campo X."
               RowErrors.ErrorType     = "ERROR".
        */
    END.
    WHEN "AFTER-SAVE" THEN DO:
        /* Integrações ou disparos pós-gravação */
    END.
END CASE.

RETURN.
```
