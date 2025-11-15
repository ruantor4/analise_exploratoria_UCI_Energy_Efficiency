#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analise_exploratoria.py
Versão didática em Português — cada parte explicada para estudo.

Objetivo:
- Ler o arquivo data/dados.csv (formato CSV)
- Mostrar estatísticas descritivas
- Verificar valores ausentes
- Gerar gráficos (histograma e heatmap de correlação)
- Gerar um relatório PDF contendo as observações e imagens

Como usar:
1. Coloque seu CSV em data/dados.csv (padrão do projeto)
2. Instale dependências: pip install -r requirements.txt
3. Execute: python src/analise_exploratoria.py
4. Resultado: outputs/relatorio_analise.pdf e imagens em outputs/

Explicação didática:
- Comentários neste arquivo explicam o propósito de cada bloco de código.
- Variáveis e funções estão em Português para facilitar o entendimento.
"""

# -------------------- Importação de bibliotecas --------------------
# pandas -> manipulação de tabelas e dados (DataFrame)
# numpy  -> operações numéricas (opcional aqui, mas comum)
# matplotlib / seaborn -> criação de gráficos
# reportlab -> criação de documentos PDF programaticamente
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os
from datetime import datetime
from textwrap import wrap

# Caminhos
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data","dados.csv")
OUTPUTS_DIR = os.path.join(BASE_PATH, "outputs")
IMAGES_DIR = os.path.join(OUTPUTS_DIR, "figs")
PDF_PATH = os.path.join(OUTPUTS_DIR, "relatorio_analise.pdf")

# Criar pastas de saída caso não existam
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)


def ler_arquivo_csv(caminho):
    """
        Lê um arquivo CSV e retorna um DataFrame do pandas.
        Se houver problemas na leitura, a função imprime mensagem de erro e encerra.
    """
    print(f"Lendo dados de: {caminho}")

    try:
        df = pd.read_csv(caminho)
        print(f"Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        return df
    except FileNotFoundError:
        print("Arquivo não encontrado. Coloque o arquivo 'dados.csv' na pasta data/")
        raise
    except Exception as e:
        print("Erro ao ler o CSV: ", e)
        raise

def renomear_colunas_pt_br(df):
     """
        Renomeia as colunas para nomes mais amigáveis em português.
        Retorna o DataFrame com as novas colunas.
    """
     map_colunas = {
        df.columns[0]: "Compacidade_Relativa",
        df.columns[1]: "Area_Superficial",
        df.columns[2]: "Area_Parede",
        df.columns[3]: "Area_Telhado",
        df.columns[4]: "Altura_Total",
        df.columns[5]: "Orientacao",
        df.columns[6]: "Area_Vidro",
        df.columns[7]: "Distribuicao_Area_Vidro",
        df.columns[8]: "Carga_Aquecimento",
        df.columns[9]: "Carga_Resfriamento",
     }
     return df.rename(columns=map_colunas)


def estatisticas_descritivas(df):
    """
        Gera e retorna um DataFrame com medidas descritivas básicas
        (contagem, média, desvio padrão, mínimos, quartis e máximos).
    """
    return df.describe()

def info(df):
     """
        Exibe informações gerais sobre o DataFrame,
        como tipos, contagem de registros e memória usada.
    """
     print("\n====== INFORMAÇÕES DO DATASET (df.info)")
     print(df.info())
     print("\n")


def verificar_nulos(df):
    """
        Retorna uma série com a contagem de valores nulos por coluna.
    """
    return df.isnull().sum()


def gerar_histogramas(df):
    """
        Gera histogramas e boxplots para cada coluna numérica do DataFrame.
        Salva as imagens em PASTA_IMAGENS.
    """
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    print("Gerando histogramas e boxplots para: ", colunas_numericas)
    
    for coluna in colunas_numericas:
        # Histograma
        plt.figure(figsize=(8,4))
        sns.histplot(df[coluna], kde=True)
        plt.title(f"Histograma - {coluna}")
        plt.xlabel(coluna)
        plt.ylabel("Frequência")
        caminho = os.path.join(IMAGES_DIR, f"hist_{coluna}.png")
        plt.tight_layout()
        plt.savefig(caminho)
        plt.close()

        # Boxplot
        plt.figure(figsize=(8,2))
        sns.boxplot(x=df[coluna])
        plt.title(f"Boxplot - {coluna}")
        caminho_box = os.path.join(IMAGES_DIR, f"box_{coluna}.png")
        plt.tight_layout()
        plt.savefig(caminho_box)
        plt.close()


def gerar_matriz_correlacao(df):
    """
        Calcula a matriz de correlação (pearson) e salva um heatmap.
        Retorna a matriz de correlação (DataFrame).
    """
    correlacao = df.corr(method="pearson")
    plt.figure(figsize=(10,8))
    sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Matriz de correlação (Pearson)")
    
    caminho = os.path.join(IMAGES_DIR, "heatmap_correlacao.png")

    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return correlacao


def extrair_maiores_correlacoes(correlacao, limite=5):
    """
        Retorna as 'limite' maiores correlações em valor absoluto entre pares de colunas,
        excluindo a diagonal (correlação de uma coluna com ela mesma).
    """
    corr = correlacao.copy().abs()
    pares = []  
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
           pares.append(((cols[i], cols[j]), corr.iloc[i, j]))
    pares_ordenados = sorted(pares, key=lambda x: x[1], reverse=True)
    return pares_ordenados[:limite]


def calcular_vif(df):
    """
        Calcula o Fator de Inflação da Variância (VIF)
        para todas as variáveis preditoras numéricas.
        
        Retorna um DataFrame com:
        - Nome da variável
        - Valor de VIF
    """
    # Selecionar apenas preditoras (remove as duas variáveis alvo)
    col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    preditoras = [c for c in col_numericas if c not in["Carga_Aquecimento", "Carga_Resfriamento"]]

    print("Calculando VIF para variaveis:")
    print(preditoras)

     # Criar matriz apenas com preditoras
    x = df[preditoras]

    # DataFrame para resultado
    vif_dados = pd.DataFrame()
    vif_dados["Variavel"] = preditoras
    vif_dados["VIF"] = [variance_inflation_factor(x.values, i) for i in range(len(preditoras))]

    print("\n ===== tabela VIF =====")
    print(vif_dados)
    
    # Salvar arquivo CSV
    caminho_csv = os.path.join(IMAGES_DIR, "vif_tabela.csv")
    vif_dados.to_csv(caminho_csv, index=False)

    return vif_dados

def scatterplots_aqueciemneto(df):
    """
        Gera scatterplots da variável alvo 'Carga_Aquecimento'
        contra todas as variáveis preditoras.
        Salva as imagens na pasta IMAGES_DIR.
    """
    target = "Carga_Aquecimento"

    # Identificar preditoras (todas as colunas numéricas menos as duas saídas)
    col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    preditoras = [col for col in col_numericas if col not in ["Carga_Aquecimento", "Carga_Resfriamento"]]

    print(f"Gerando scatterplots de {target} para as variáveis:")
    print(preditoras)

    for col in preditoras:
        plt.figure(figsize=(6,4))
        sns.scatterplot(x=df[col], y=df[target])
        plt.title(f"{col} vs {target}")
        plt.xlabel(col)
        plt.ylabel(target)
        
        caminho = os.path.join(IMAGES_DIR, f"scatter_{target}_{col}.png")
        
        plt.tight_layout()
        plt.savefig(caminho)
        plt.close()

def scatterplots_refriamento(df):
    """
        Gera scatterplots da variável alvo 'Carga_Resfriamento'
        contra todas as variáveis preditoras.
        Salva as imagens na pasta IMAGES_DIR.
    """
    target = "Carga_Resfriamento"

    # Identificar todas as colunas numéricas
    col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

    # Remover as duas variáveis-alvo para obter apenas preditoras
    preditores = [col for col in col_numericas if col not in ["Carga_Aquecimento", "Carga_Resfriamento"]]

    print(f"Gerando scatterplots de {target} para as variáveis:")
    print(preditores)

    for col in preditores:
        plt.figure(figsize=(6,4))
        sns.scatterplot(x=df[col], y=df[target])
        plt.title(f"Scatterplot de {col} vs {target}")
        plt.xlabel(col)
        plt.ylabel(target)

        caminho = os.path.join(IMAGES_DIR, f"scatter_{target}_{col}.png")
        plt.tight_layout()
        plt.savefig(caminho)
        plt.close()

def gerar_relatorio_pdf(df, descricao, nulos, correlacao, maiores_correlacoes):
    """
    Gera um relatório em PDF com:
    - Info (df.info)
    - Sumário executivo
    - Estatísticas descritivas
    - Valores nulos
    - Maiores correlações
    - Heatmap de correlação
    - Histogramas
    - Boxplots
    - Scatterplots aquecimento e resfriamento
    - Tabela VIF
    """
    print("Gerando PDF...")
    largura, altura = A4
    c = canvas.Canvas(PDF_PATH, pagesize=A4)

    # ---------- CAPA ----------
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(largura / 2, altura - 80, "Relatório de Análise Exploratória")
    c.setFont("Helvetica", 12)
    c.drawCentredString(
        largura / 2,
        altura - 100,
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    c.showPage()

    # ---------- INFO ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Tabela 1: Info do Dataset")
    c.setFont("Courier", 9)

    # >>> CORREÇÃO AQUI: usar StringIO em vez de buffer.append <<<
    buffer_info = StringIO()
    df.info(buf=buffer_info)
    linhas = buffer_info.getvalue().split("\n")

    y = altura - 90
    for linha in linhas:
        c.drawString(40, y, linha)
        y -= 10
        if y < 60:
            c.showPage()
            c.setFont("Courier", 9)
            y = altura - 60

    c.showPage()

    # ---------- SUMÁRIO EXECUTIVO ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Sumário Executivo")
    c.setFont("Helvetica", 11)
    c.drawString(40, altura - 90, f"Total de registros: {df.shape[0]}")
    c.drawString(40, altura - 108, f"Total de colunas: {df.shape[1]}")
    c.drawString(
        40,
        altura - 126,
        "As próximas seções detalham os achados da análise exploratória."
    )
    c.showPage()

   # ---------- DESCRIBE ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Tabela 2: Estatísticas Descritivas")
    c.setFont("Courier", 8)

    # Transformar estatísticas para formato vertical (tipo tabela)
    descricao_vertical = descricao.T  # transpor a tabela
    linhas = descricao_vertical.to_string().split("\n")

    y = altura - 90

    for linha in linhas:
        c.drawString(40, y, linha)
        y -= 10

        # quebra de página automática
        if y < 60:
            c.showPage()
            c.setFont("Courier", 8)
            y = altura - 60

    # ---------- VALORES NULOS ----------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Valores Nulos")
    c.setFont("Helvetica", 11)

    y = altura - 90
    for col, val in nulos.items():
        c.drawString(40, y, f"- {col}: {val}")
        y -= 14
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = altura - 60

    # ---------- MAIORES CORRELAÇÕES ----------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Maiores Correlações")
    c.setFont("Helvetica", 11)
    y = altura - 90

    for (a, b), val in maiores_correlacoes:
        c.drawString(40, y, f"- {a} ↔ {b}: {val:.4f}")
        y -= 14
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = altura - 60

    # ---------- HEATMAP ----------
    caminho_heat = os.path.join(IMAGES_DIR, "heatmap_correlacao.png")
    if os.path.exists(caminho_heat):
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, altura - 60, "Figura 3: Matriz de Correlação")

        img = ImageReader(caminho_heat)
        iw, ih = img.getSize()
        img_w = largura - 80
        img_h = img_w * (ih / iw)

        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- HISTOGRAMAS ----------
    if os.path.exists(IMAGES_DIR):
        imagens_hist = [
            f for f in os.listdir(IMAGES_DIR)
            if f.startswith("hist_")
        ]
    else:
        imagens_hist = []

    for fname in imagens_hist:
        caminho_img = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(caminho_img):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, altura - 60, f"Figura: {fname}")
            img = ImageReader(caminho_img)

            iw, ih = img.getSize()
            img_w = largura - 80
            img_h = img_w * (ih / iw)
            c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- BOXPLOTS ----------
    if os.path.exists(IMAGES_DIR):
        imagens_box = [
            f for f in os.listdir(IMAGES_DIR)
            if f.startswith("box_")
        ]
    else:
        imagens_box = []

    for fname in imagens_box:
        caminho_img = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(caminho_img):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, altura - 60, f"Figura: {fname}")
            img = ImageReader(caminho_img)

            iw, ih = img.getSize()
            img_w = largura - 80
            img_h = img_w * (ih / iw)
            c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- SCATTERPLOTS AQUECIMENTO ----------
    if os.path.exists(IMAGES_DIR):
        imagens_scatter_aq = [
            f for f in os.listdir(IMAGES_DIR)
            if f.startswith("scatter_Carga_Aquecimento")
        ]
    else:
        imagens_scatter_aq = []

    for fname in imagens_scatter_aq:
        caminho_img = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(caminho_img):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, altura - 60, f"Figura: {fname}")
            img = ImageReader(caminho_img)

            iw, ih = img.getSize()
            img_w = largura - 80
            img_h = img_w * (ih / iw)
            c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- SCATTERPLOTS RESFRIAMENTO ----------
    if os.path.exists(IMAGES_DIR):
        imagens_scatter_res = [
            f for f in os.listdir(IMAGES_DIR)
            if f.startswith("scatter_Carga_Resfriamento")
        ]
    else:
        imagens_scatter_res = []

    for fname in imagens_scatter_res:
        caminho_img = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(caminho_img):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, altura - 60, f"Figura: {fname}")
            img = ImageReader(caminho_img)

            iw, ih = img.getSize()
            img_w = largura - 80
            img_h = img_w * (ih / iw)
            c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- VIF ----------
    caminho_vif = os.path.join(IMAGES_DIR, "vif_tabela.csv")

    if os.path.exists(caminho_vif):
        vif_df = pd.read_csv(caminho_vif)

        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, altura - 60, "Tabela 3: Fator de Inflação da Variância (VIF)")
        c.setFont("Courier", 9)

        y = altura - 90
        linhas = vif_df.to_string(index=False).split("\n")
        for linha in linhas:
            c.drawString(40, y, linha)
            y -= 12
            if y < 60:
                c.showPage()
                c.setFont("Courier", 9)
                y = altura - 60

    c.save()
    print(f"PDF salvo em: {PDF_PATH}")
