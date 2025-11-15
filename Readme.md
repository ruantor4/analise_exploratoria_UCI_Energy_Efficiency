# Análise Exploratória: Eficiência Energética

Aplicação desenvolvida em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** para realizar **[análise exploratória de dados (EDA)](https://pt.wikipedia.org/wiki/An%C3%A1lise_explorat%C3%B3ria_de_dados)**  como parte da **Prova de Conceito (PoC)** de um sistema preditivo para **eficiência energética de edifícios**, com base no conjunto de dados público **[UCI Energy Efficiency Dataset](https://archive.ics.uci.edu/ml/datasets/energy+efficiency)**.

Baseia-se no conjunto de dados público **[UCI Energy Efficiency Dataset](https://archive.ics.uci.edu/ml/datasets/energy+efficiency)**., realizando uma análise exploratória completa (EDA) para entender padrões, distribuições e relações entre variáveis, preparando o terreno para modelos de Machine Learning.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**
## Objetivos do Projeto

- Converter o arquivo original em Excel (`ENB2012_data.xlsx`) para CSV (`dados.csv`).
- Explorar estatisticamente o dataset: médias, desvios, quartis, amplitude etc.
- Verificar valores ausentes.
- Calcular correlações e extrair as variáveis mais relacionadas.
- Gerar visualizações como histogramas, boxplots, scatterplots e heatmaps.
- Compilar automaticamente um **relatório completo em PDF** com todos os resultados.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**


## Funcionalidades

| Categoria | Descrição |
|----------|-----------|
| **Conversão de Arquivos** | Transforma o `ENB2012_data.xlsx` em `dados.csv` automaticamente. |
| **Leitura e Validação dos Dados** | Importa o CSV e valida estrutura e consistência. |
| **Estatísticas Descritivas** | Gera métricas estatísticas para todas as variáveis numéricas. |
| **Detecção de Valores Ausentes** | Conta e exibe atributos com dados faltantes. |
| **Análise de Correlação** | Calcula matriz de correlação entre variáveis. |
| **Maiores Correlações** | Identifica os pares mais correlacionados. |
| **Visualizações** | Histogramas, boxplots, heatmaps e scatterplots. |
| **Relatório PDF Automatizado** | Gera `outputs/relatorio_analise.pdf` com tabelas e gráficos. |
| **Criação Automática de Pastas** | Organiza saídas em `outputs/` e `outputs/figs/`. |



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**
## Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| Manipulação de Dados | **[pandas](https://pandas.pydata.org/docs/)**, **[numpy](https://numpy.org/doc/)** |
| Visualização | **[matplotlib](https://matplotlib.org/stable/users/explain/quick_start.html)**, **[seaborn](https://seaborn.pydata.org/)** |
| Relatórios PDF | **[reportlab](https://docs.reportlab.com/releases/notes/whats-new-40/)** |
| Utilidades | **[os](https://docs.python.org/pt-br/3/library/os.html)**, **[datetime](https://docs.python.org/pt-br/3/library/datetime.html)**, **[textwrap](https://docs.python.org/pt-br/dev/library/textwrap.html)** |

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Estrutura de Diretórios

```
eficiencia_energetica_AT1/
├── data/
│   ├── ENB2012_data.xlsx         # Arquivo original
│   └── dados.csv                 # Criado automaticamente
│
├── outputs/
│   ├── figs/                     # Gráficos gerados
│   └── relatorio_analise.pdf     # Relatório em PDF
│
├── src/
│   ├── convert_csv.py            # Conversão XLSX → CSV
│   ├── analise_exploratoria.py   # Funções de análise + PDF
│   ├── main.py                   # Execução principal do projeto
│
├── requirements.txt              # Dependências
└── README.md                     # Documentação
```
**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Instalação e Execução

### Passo 1 – Criar o ambiente virtual
```bash
$ python -m venv .venv
$ source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
```

### Passo 2 – Instalar dependências
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Passo 3 – Execute o Projeto
```bash
$ python src/main.py
```
> Isso cria automaticamente `data/dados.csv` e inicia o projeto.



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## 📊 Estrutura do Relatório PDF


O relatório final (outputs/relatorio_analise.pdf) contém:

* **Informações do dataset (df.info())**
* **Estatísticas descritivas em formato vertical**
* **Quantidade de valores ausentes**
* **Matriz de correlação completa**
* **Top 5 correlações mais fortes**
* **Histogramas de todas as variáveis**
* **Boxplot**
* **Scatterplots para aquecimento e resfriamento**
* **Heatmap da matriz de correlação**
* **Tabela VIF (caso gerada)**


