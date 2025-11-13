# Análise Exploratória: Eficiência Energética

Aplicação desenvolvida em **Python** para realizar **análise exploratória de dados (EDA)**  como parte da **Prova de Conceito (PoC)** de um sistema preditivo para **eficiência energética de edifícios**, com base no conjunto de dados público **[UCI Energy Efficiency Dataset](https://archive.ics.uci.edu/ml/datasets/energy+efficiency)**.

O objetivo deste projeto é **analisar e compreender os dados**, verificando distribuições, correlações e padrões relevantes que auxiliem na criação de modelos preditivos.

---
## 📋 Objetivos do Projeto

- Ler e converter dados originais no formato **Excel (.xlsx)** para **CSV (.csv)**.  
- Explorar o conjunto de dados com **estatísticas descritivas** e **análise de correlação**.  
- Visualizar padrões e relações entre variáveis usando **gráficos e heatmaps**.  
- Documentar automaticamente os resultados em um **relatório PDF**.  

---

## ⚙️ Funcionalidades

| Categoria | Descrição |
|------------|------------|
| **Conversão de Arquivos** | Lê o arquivo `ENB2012_data.xlsx` e converte para `dados.csv` automaticamente. |
| **Leitura de Dados** | Utiliza o `pandas` para importar e validar o CSV convertido. |
| **Estatísticas Descritivas** | Gera medidas como média, mediana, desvio padrão, mínimo e máximo para cada atributo. |
| **Detecção de Valores Ausentes** | Verifica e contabiliza dados faltantes ou inconsistentes. |
| **Análise de Correlação** | Calcula e exibe a matriz de correlação entre variáveis numéricas. |
| **Extração das Maiores Correlações** | Identifica os pares de atributos mais relacionados usando a função `extrair_maiores_correlacoes()`. |
| **Visualizações Gráficas** | Cria histogramas e mapas de calor (`heatmaps`) com `matplotlib` e `seaborn`. |
| **Geração de Relatório PDF** | Compila resultados e gráficos em `outputs/relatorio_analise.pdf`. |
| **Criação Automática de Pastas** | Estrutura as saídas em diretórios organizados (`data/`, `outputs/`, `outputs/figs/`). |

---

## 🧰 Stack e Dependências

| Categoria | Tecnologia / Biblioteca |
|------------|------------------------|
| Manipulação de Dados | [**pandas**](https://pandas.pydata.org/) |
| Visualização | [**matplotlib**](https://matplotlib.org/), [**seaborn**](https://seaborn.pydata.org/) |
| Exportação e Relatórios | [**reportlab**](https://www.reportlab.com/dev/docs/reportlab-userguide.pdf) |
| Utilitários | [**os**, **datetime**, **numpy**] |

---

## 📂 Estrutura de Diretórios

```
eficiencia_energetica_AT1/
├── data/
│   ├── ENB2012_data.xlsx        # Arquivo original
│   └── dados.csv                # Arquivo convertido 
│
├── outputs/
│   ├── figs/                    # Figuras e gráficos gerados
│   └── relatorio_analise.pdf    # Relatório final em PDF
│
├── src/
│   ├── convert_csv.py           # Conversão de XLSX para CSV
│   ├── analise_exploratoria.py  # Análise e geração de relatório
│
├── requirements.txt             # Dependências do projeto
└── README.md                    # Documentação do projeto
```

---

## ⚙️ Instalação e Execução

### 🔹 Passo 1 – Criar o ambiente virtual
```bash
$ python -m venv .venv
$ source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
```

### 🔹 Passo 2 – Instalar dependências
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### 🔹 Passo 3 – Converter o arquivo Excel em CSV
```bash
$ python src/convert_csv.py
```
> Isso cria automaticamente `data/dados.csv`.

### 🔹 Passo 4 – Executar a análise exploratória
```bash
$ python src/analise_exploratoria.py
```
> As saídas serão salvas em `outputs/` e o relatório em PDF estará disponível em:
> ```
> outputs/relatorio_analise.pdf
> ```

---

## 📊 Estrutura do Relatório Gerado

O relatório contém:

1. **Informações gerais do dataset**  
2. **Estatísticas descritivas detalhadas**  
3. **Valores ausentes**  
4. **Matriz de correlação completa**  
5. **Top 5 correlações mais fortes**  
6. **Visualizações (gráficos e heatmaps)**  

---

