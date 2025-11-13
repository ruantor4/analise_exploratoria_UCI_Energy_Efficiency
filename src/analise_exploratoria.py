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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime

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


def extrair_maiores_correlaçoes(correlacao, limite=5):
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


def gerar_relatorio_pdf(df, descricao, nulos, correlacao, maiores_correlacoes):
    """
    Gera um relatório em PDF com:
    - Capa com título e data
    - Sumário executivo com número de registros e colunas
    - Resumo estatístico (texto)
    - Tabela de valores nulos
    - Lista das maiores correlações
    - Inserção da imagem do heatmap de correlação
    - Inserção de alguns histogramas (até 4 primeiras imagens encontradas)
    """
    print("Gerando PDF...")
    largura, altura = A4
    c = canvas.Canvas(PDF_PATH, pagesize=A4)

   # Capa
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(largura / 2, altura - 80, "Relatório de Análise Exploratória")
    c.setFont("Helvetica", 12)
    c.drawCentredString(largura / 2, altura - 100, f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.showPage()

    # Sumário Executivo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Sumário Executivo")
    c.setFont("Helvetica", 11)
    c.drawString(40, altura - 80, f"Total de registros: {df.shape[0]}")
    c.drawString(40, altura - 98, f"Total de colunas: {df.shape[1]}")
    c.drawString(40, altura - 116, "Observações: ver se há valores nulos e as maiores correlações abaixo.")
    c.showPage()

    # Resumo Estatísco
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura-60, "Resumo Estatístico (numérico)")
    c.setFont("Courier", 9)
    texto = descricao.to_string()
    linhas = texto.split("\n")
    y = altura - 90
    for linha in linhas:
        c.drawString(40, y, linha)
        y -= 10
        if y < 60:
            c.showPage()
            y = altura - 60

    # Valores Nulos
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Contagem de Valores Nulos por Coluna")
    c.setFont("Helvetica", 11)
    
    y = altura - 90
    
    for col, val in nulos.items():
        c.drawString(40, y, f"- {col}: {int(val)}")
        y -= 14
        if y < 60:
            c.showPage()
            y = altura - 60

    # Maiores correlações
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Maiores Correlações (valor absoluto)")
    c.setFont("Helvetica", 11)

    y = altura - 90

    if len(maiores_correlacoes) == 0:
        c.drawString(40, y, "Nenhuma correlação alta encontrada.")
    else:
        for (a,b), val in maiores_correlacoes:
            c.drawString(40, y, f"- {a} ↔ {b} : {val:.2f}")
            y -= 14
            if y < 60:
                c.showPage()
                y = altura - 60


    # Inserir headMap de correlação
    caminho_heat = os.path.join(IMAGES_DIR, "heatmap_correlacao.png")
    
    if os.path.exists(caminho_heat):
        
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, altura - 60 , "Heatmap de Correlação")
        
        img = ImageReader(caminho_heat)

        iw, ih = img.getSize()
        aspect = ih / iw
        img_w = largura - 80
        img_h = img_w * aspect
        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # Inserir até 4 histogramas como exemplo
    imagens = [f for f in os.listdir(IMAGES_DIR) if f.startswith("hist_")][:4]
    
    for img_name in imagens:
        caminho_img = os.path.join(IMAGES_DIR, img_name)
            
        if os.path.exists(caminho_img):
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, altura - 60, f"Visualização: {img_name}")
            img = ImageReader(caminho_img)
            iw, ih = img.getSize()
            aspect = ih/iw
            img_w = largura - 80
            img_h = img_w * aspect
            c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    c.save()
    print(f"PDF salvo em: {PDF_PATH}")

    # ---- FLUXO DE EXECUÇÃO ----
def main():
    # Ler dados
    df = ler_arquivo_csv(DATA_PATH)

    # Renomear colunas para portuguès
    df = renomear_colunas_pt_br(df)

    # Estatisticas descritivas
    descricao = estatisticas_descritivas(df)

    # Verificar nulos
    nulos = verificar_nulos(df)

    # Gerar gráficos
    gerar_histogramas(df)
    
    correl = gerar_matriz_correlacao(df)

    # Extrair maiores correlações
    maiores = extrair_maiores_correlaçoes(correl, limite=6)

    # Gerar PDF
    gerar_relatorio_pdf(df, descricao, nulos, correl, maiores)


if __name__ == "__main__":
    main()