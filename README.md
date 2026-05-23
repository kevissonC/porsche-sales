# 🏎️ Porsche Sales Intelligence Dashboard

Dashboard interativo de análise de vendas da Porsche, gerado a partir de um banco de dados `.xlsx` com dados sanitizados. Desenvolvido como projeto prático da trilha **Aceleração Excel com IA** — Santander Open Academy / DIO.

---

## 📸 Preview

> Dashboard com tema escuro inspirado no site oficial da [Porsche Brasil](https://www.porsche.com/brazil/pt/), com paleta dourada, tipografia refinada e gráficos interativos.

---

## 📁 Estrutura do Repositório

```
.
├── porsche_dashboard.py           # Script Python que gera o dashboard
├── porsche_dashboard.html         # Dashboard gerado (output)
├── material-complementar/
│   └── porsche-database-v2.xlsx   # Banco de dados de vendas (sanitizado)
└── schema.md                      # Schema de sanitização do banco de dados
```

---

## ⚙️ Requisitos

- Python 3.8+
- pandas
- openpyxl

Instale as dependências com:

```bash
pip install pandas openpyxl
```

---

## 🚀 Como usar

```bash
python porsche_dashboard.py <caminho_do_xlsx> <caminho_do_output_html>
```

**Exemplo:**

```bash
python porsche_dashboard.py "material-complementar/porsche-database-v2.xlsx" porsche_dashboard.html
```

O script lê o `.xlsx`, processa os dados e gera um arquivo `.html` completo e autocontido — sem dependências externas de servidor.

---

## 📊 Funcionalidades do Dashboard

### Filtros interativos
| Filtro | Descrição |
|---|---|
| Modelo | Filtra por modelo da Porsche (911, Taycan, Macan…) |
| Model Year | Filtra por ano do veículo |
| Cidade | Filtra por cidade de venda |
| Forma de pagamento | Filtra por método (Cash, Financing, Wire Transfer…) |

Todos os filtros são combinados em tempo real — KPIs, gráficos e tabela atualizam instantaneamente.

### KPIs
- **Total de vendas** — quantidade de registros filtrados
- **Receita total** — soma dos preços de venda
- **Ticket médio** — receita ÷ unidades
- **Cidades ativas** — mercados presentes nos dados filtrados

### Visualizações
- **Modelos mais vendidos por cidade** — barras empilhadas
- **Distribuição por ano de modelo** — barras agrupadas
- **Mix de pagamentos** — gráfico donut
- **Receita por modelo** — barras horizontais ranqueadas

### Insights de mercado
Cards automáticos com o modelo líder em cada cidade, quantidade vendida e ticket médio local.

### Tabela de transações
Listagem das transações filtradas com badge de status (Delivered / In Transit / Pending).

---

## 🗄️ Schema do Banco de Dados

O arquivo `schema.md` documenta as regras de sanitização aplicadas ao banco bruto para gerar o `.xlsx` utilizado pelo dashboard.

### Colunas sanitizadas

| Coluna original | Coluna sanitizada | Formato |
|---|---|---|
| `sale_date` | `SaleDateSanitized` | `YYYY-MM-DD` ou `INVALID` |
| `porsche_model` | `PorscheModelSanitized` | Label canônico do modelo |
| `model_year` | `ModelYearSanitized` | Ano com 4 dígitos ou `INVALID` |
| `sale_price` | `SalesPriceSanitized` | Valor decimal em USD |
| `vehicle_mileage` | `VehicleMileageSanitized` | Inteiro em milhas |
| `payment_method` | `PayMethodSanitized` | Label controlado |
| `city` | `CitySanitized` | Title case |
| `state` | `StateSanitized` | Código USPS de 2 letras ou `INVALID` |
| `delivery_status` | `DeliveryStatusSanitized` | Label controlado |

### Principais regras de tratamento
- **Datas** — normalizadas para ISO `YYYY-MM-DD`; datas inválidas no calendário viram `INVALID`
- **Preços** — aceita formatos como `$645k`, `188k USD`, `eighty two thousand USD`; normaliza para decimal sem símbolos
- **Quilometragem** — suporta milhas e km (convertido com `1 km = 0.621371 mi`); textos como `new` ou `zero miles` viram `0`
- **Estado** — converte nomes completos e abreviações para código USPS de 2 letras
- **Status de entrega** — normaliza variações de caixa, hifenização e typos comuns (ex: `DELIVERD` → `Delivered`)
- **Valores não normalizáveis** — nunca ficam em branco; recebem `INVALID`

---

## 🎨 Design

Inspirado no site oficial da Porsche Brasil, o dashboard segue uma identidade visual de luxo:

- Paleta **preto profundo** (`#0a0a0a`) com acento **dourado** (`#c9a84c`)
- Tipografia **Cormorant Garamond** (display) + **DM Sans** (corpo)
- Layout de grade com bordas sutis e hover states refinados
- Watermark tipográfica em background

---

## 📝 Sobre o Projeto

Projeto desenvolvido durante a trilha **Aceleração Excel com IA** promovida pela [DIO](https://www.dio.me/) em parceria com o **Santander Open Academy**.

O objetivo foi transformar um banco de dados de vendas com dados sujos em um dashboard executivo completo, cobrindo desde a sanitização dos dados até a visualização interativa.

---

## 📄 Licença

Este projeto é de uso educacional e foi desenvolvido como exercício prático da trilha DIO/Santander.
