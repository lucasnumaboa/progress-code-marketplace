---
name: conversor-telas-datasul-poui
description: Use esta skill para modernizar e converter automaticamente telas legadas do TOTVS Datasul (.w, ChUI em modo caracter ou GUI clássico Progress ABL) para aplicações Web modernas em Angular 17 + PO-UI 17 prontas para rodar no Tomcat/PASOE do Datasul. Inclui template e scaffold zipado (po-ui.zip) com script de build de WAR automatizado.
modelInvocable: true
---

# Conversor de Telas Datasul (.w / ChUI) para Web Moderna (PO-UI)

Esta skill permite converter telas legadas Progress OpenEdge / Datasul (`.w`, telas caracter ChUI, janelas AppBuilder, dialogs e cadastros) para interfaces modernas e responsivas utilizando a biblioteca oficial **TOTVS PO-UI (Angular 17)** consumindo APIs REST no PASOE.

---

## Estrutura do Pacote e Template Base

A skill já acompanha o scaffold completo zipado em `template/po-ui.zip` (com Angular 17, PO-UI 17, interceptor de autenticação JWT Datasul, temas visuais oficiais e script `build_projeto.bat` para empacotamento em `.war`).

### Como Inicializar o Projeto a Partir do Template
1. Descompacte o arquivo `template/po-ui.zip` na pasta de trabalho do projeto.
2. Acesse a pasta `po-ui/` gerada.
3. Instale as dependências:
   ```bash
   npm install --legacy-peer-deps
   ```
4. Para testar localmente em desenvolvimento:
   ```bash
   npm start
   ```
5. Para compilar e gerar o `.war` do Datasul:
   ```bash
   build_projeto.bat
   ```

---

## 1. Mapeamento de Widgets Progress ABL → Componentes PO-UI

Ao analisar um arquivo `.w` ou rotina de tela Progress, aplique a seguinte tabela de conversão arquitetural:

| Elemento Progress / Datasul | Componente PO-UI Equivalente | Propriedades e Recursos Chave |
|---|---|---|
| **BROWSE** de dados | `<po-table>` | `[p-columns]`, `[p-items]`, `[p-actions]`, ordenação, filtro rápido e paginação. |
| **FRAME** / Janela Principal | `<po-page-default>` ou `<po-page-edit>` | `p-title`, `[p-breadcrumb]`, `[p-actions]`. |
| **FILL-IN** de texto/código | `<po-input>` | `p-label`, `p-placeholder`, `p-required`, `p-maxlength`. |
| **FILL-IN** numérico / moeda | `<po-number>` ou `<po-decimal>` | `p-decimals`, `p-min`, `p-max`, `p-icon`. |
| **FILL-IN** de data | `<po-datepicker>` | `p-format="dd/mm/yyyy"`, validação de intervalo. |
| **COMBO-BOX** fixo | `<po-select>` | `[p-options]="[{ label, value }]"` |
| **RADIO-SET** | `<po-radio-group>` | `[p-options]`, layout horizontal ou vertical. |
| **TOGGLE-BOX** (Sim/Não) | `<po-switch>` | `p-label-off="Não"`, `p-label-on="Sim"`. |
| **EDITOR** / Observações | `<po-textarea>` | `[p-rows]="4"`, contagem de caracteres. |
| **BUTTON** de ação | `<po-button>` | `p-kind="primary"`, `p-kind="danger"`, `(p-click)`. |
| **DIALOG-BOX** / Mensagens de aviso | `<po-modal>` ou `PoNotificationService` | Alertas `success`, `warning`, `error`, `information`. |
| **Pesquisa / Zoom (F5)** | `<po-lookup>` ou `<po-combo>` | `p-filter-service`, busca assíncrona por código ou descrição. |

---

## 2. Passo a Passo da Conversão

### Passo 1: Leitura e Engenharia Reversa do `.w`
1. **Definição de Temp-Tables:** Identifique as tabelas de trabalho (`DEF TEMP-TABLE tt-dados...`) e campos de tela.
2. **Definição de Frames e Campos:** Analise o bloco `&ANALYZE-SUSPEND _UIB-CODE-BLOCK _CUSTOM _DEFINITIONS` e `FORM ... WITH FRAME`.
3. **Mapeamento de Gatilhos (Triggers):**
   - `ON 'CHOOSE' OF bt-salvar`: Mapeia para o método `salvar()` no componente Angular.
   - `ON 'LEAVE' OF fi-codigo`: Mapeia para `(p-change)` ou validação reativa no Form.
   - `ON 'ROW-LEAVE' OF br-dados`: Mapeia para ação de linha da `<po-table>`.

### Passo 2: Construção da API REST Progress (PASOE)
Gere uma procedure `.p` no backend Datasul que expõe os dados em JSON:
```progress
/* backend/api/v1/servico.p */
@openapi.openedge.export FILE(type="REST", restResource="", version="1.0").
BLOCK-LEVEL ON ERROR UNDO, THROW.

DEFINE TEMP-TABLE tt-registro NO-UNDO
    FIELD cod-chave    AS CHARACTER
    FIELD des-nome     AS CHARACTER
    FIELD val-total    AS DECIMAL
    FIELD dat-cadastro AS DATE.

DEFINE DATASET dsRegistros FOR tt-registro.

PROCEDURE getRegistros:
    DEFINE OUTPUT PARAMETER DATASET FOR dsRegistros.
    
    /* Leitura do banco Datasul com tratamento de locking */
    FOR EACH tabela NO-LOCK:
        CREATE tt-registro.
        BUFFER-COPY tabela TO tt-registro.
    END.
END PROCEDURE.
```

### Passo 3: Geração do Componente Angular + PO-UI
Crie o componente da tela com HTML declarativo e TypeScript estruturado:
```html
<po-page-default [p-title]="titulo" [p-actions]="pageActions">
  <po-table
    [p-columns]="columns"
    [p-items]="items"
    [p-loading]="isLoading"
    [p-actions]="tableActions">
  </po-table>
</po-page-default>
```

```typescript
@Component({
  selector: 'app-tela-convertida',
  templateUrl: './tela-convertida.component.html'
})
export class TelaConvertidaComponent implements OnInit {
  items: any[] = [];
  isLoading = false;
  columns: PoTableColumn[] = [
    { property: 'codChave', label: 'Código', width: '120px' },
    { property: 'desNome', label: 'Descrição' },
    { property: 'valTotal', label: 'Valor', type: 'currency', format: 'BRL' },
    { property: 'datCadastro', label: 'Data', type: 'date' }
  ];

  constructor(
    private service: TelaConvertidaService,
    private poNotification: PoNotificationService
  ) {}

  ngOnInit() {
    this.carregarDados();
  }

  carregarDados() {
    this.isLoading = true;
    this.service.buscarRegistros().subscribe({
      next: (res) => {
        this.items = res.items;
        this.isLoading = false;
      },
      error: (err) => {
        this.poNotification.error('Erro ao consultar dados no Datasul: ' + err.message);
        this.isLoading = false;
      }
    });
  }
}
```

### Passo 4: Autenticação e Deploy no Datasul
- O arquivo `auth.interceptor.ts` incluso no template intercepta as requisições HTTP e injeta automaticamente o token JWT da sessão ativa do menu web do TOTVS Datasul.
- Ao rodar `build_projeto.bat`, o arquivo `.war` é gerado na raiz e pode ser copiado diretamente para `webapps/` do Tomcat do Datasul.
