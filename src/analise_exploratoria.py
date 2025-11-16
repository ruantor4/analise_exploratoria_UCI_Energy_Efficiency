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
import logging
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

def ler_arquivo_csv(caminho :str) -> pd.DataFrame:
    """
        Lê um arquivo CSV e retorna um DataFrame do pandas.
        Se houver problemas na leitura, a função imprime mensagem de erro e encerra.
    """
    logging.info(f"Lendo dados de: {caminho}")

    try:
        df = pd.read_csv(caminho)

    except FileNotFoundError:
        logging.error("Arquivo não encontrado. Coloque o arquivo 'dados.csv' na pasta data/")
        raise
    except Exception as e:
        logging.error("Erro ao ler o CSV: ", e)
        raise
    
    logging.info(f"Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
    
    return df


def renomear_colunas_pt_br(df: pd.DataFrame) -> pd.DataFrame:
    """
        Renomeia as colunas para nomes mais amigáveis em português.
        Retorna o DataFrame com as colunas renomeadas.
    """
    logging.info("Renomeando colunas para o padrão em português...")

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
    df_renomeado = df.rename(columns=map_colunas)
    
    logging.info("Colunas renomeadas com sucesso.")
    logging.debug(f"Novos nomes das colunas: {df_renomeado.columns.tolist()}")
    
    return df_renomeado


def estatisticas_descritivas(df):
    """
    Calcula e retorna estatísticas descritivas para todas
    as variáveis numéricas do DataFrame.

    As estatísticas incluem:
    - count
    - mean
    - std
    - min
    - 25%, 50%, 75%
    - max

    Retorna:
        DataFrame com as estatísticas descritivas.
    """
    logging.info("Calculando as estatísticas decritivas...")

    try:
        descricao = df.describe()
    
    except Exception:
        logging.error("Erro ao gerar estatísticas desritivas", exc_info=True)
        raise

    logging.info("Estatísticas descritivas calculadas com sucesso.")
    
    return descricao


def info(df: pd.DataFrame) -> str:
    """
    Captura e retorna as informações do DataFrame no formato string,
    equivalente ao df.info(), porém sem imprimir no console.

    Isso permite:
    - registrar info em logs
    - incluir info no relatório PDF
    - testar info programaticamente

    Retorna:
        str contendo o resultado do df.info()
    """
    logging.info("Gerando informações do DataFrame (df.info)...")

    try:
        buffer = StringIO()
        df.info(buf=buffer)
        resultado = buffer.getvalue()

    except Exception:
        logging.error("Erro ao executar df.info()", exc_info=True)
        raise

    return resultado


def verificar_nulos(df:pd.DataFrame) -> pd.Series:
    """
    Verifica e retorna a quantidade de valores nulos por coluna no DataFrame.

    Retorna:
        pandas.Series contendo o nome da coluna e a quantidade de valores nulos.
    """

    logging.info("Verificando valores nulos nas colunas...")

    try:
        nulos = df.isnull().sum()

    except Exception:
        logging.error("Erro ao verificar valores nulos.", exc_info=True)
        raise

    logging.info("Verificação de valores nulos concluída.")

    return nulos


def gerar_histogramas(df: pd.DataFrame, images_dir: str) -> None:
    """
    Gera histogramas e boxplots para todas as variáveis numéricas.
    Cada gráfico é salvo como imagem PNG dentro do diretório especificado.

    Parâmetros:
        df (DataFrame): conjunto de dados já pré-processado.
        images_dir (str): diretório onde as imagens serão salvas.

    Retorno:
        None (gera arquivos .png no disco)
    """

    logging.info("Gerando histogramas e boxplots para variáveis numéricas...")


    try:
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    except Exception:
        logging.error("Erro ao identificar colunas numéricas.", exc_info=True)
        raise

    # Geração dos gráficos
    for coluna in colunas_numericas:
        
        try:
            # Histograma
            plt.figure(figsize=(8,4))
            sns.histplot(df[coluna], kde=True)
            plt.title(f"Histograma - {coluna}")
            plt.xlabel(coluna)
            plt.ylabel("Frequência")
            
            caminho = os.path.join(images_dir, f"hist_{coluna}.png")
            plt.tight_layout()
            plt.savefig(caminho)
            plt.close()

            logging.debug(f"Histograma salvo: {caminho}")

            # Boxplot
            plt.figure(figsize=(8,2))
            sns.boxplot(x=df[coluna])
            plt.title(f"Boxplot - {coluna}")
            
            caminho_box = os.path.join(images_dir, f"box_{coluna}.png")
            plt.tight_layout()
            plt.savefig(caminho_box)
            plt.close()
        
        except Exception:
            logging.error(f"Erro ao gerar gráficos para a coluna: {coluna}", exc_info=True)
            raise

        logging.info("Histogramas e boxplots gerados com sucesso.")


def gerar_matriz_correlacao(df: pd.DataFrame, images_dir: str) -> pd.DataFrame:
    """
    Calcula a matriz de correlação (método Pearson) para as variáveis numéricas
    e salva o heatmap correspondente no diretório fornecido.

    Parâmetros:
        df (DataFrame): conjunto de dados processado.
        images_dir (str): diretório onde o heatmap será salvo.

    Retorna:
        DataFrame contendo a matriz de correlação.
    """
    logging.info("Calculando matriz de correlação (Pearson)...")

    try:
        correlacao = df.corr(method="pearson")

    except Exception:
        logging.error("Erro ao calcular matriz de correlação.", exc_info=True)
        raise
    
    try:
        plt.figure(figsize=(10,8))
        sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Matriz de correlação (Pearson)")
    
        caminho = os.path.join(images_dir, "heatmap_correlacao.png")

        plt.tight_layout()
        plt.savefig(caminho)
        plt.close()

    except Exception:
        logging.error(f"Heatmap de correlação salvo em: {caminho}")
    
    return correlacao


def extrair_maiores_correlacoes(correlacao: pd.DataFrame, limite: int = 5):
    """
    Retorna os pares de variáveis com maiores correlações absolutas,
    excluindo a diagonal (correlação da variável consigo mesma).

    Parâmetros:
        correlacao (DataFrame): matriz de correlação.
        limite (int): quantidade de pares mais fortes a retornar.

    Retorna:
        Lista de tuplas no formato:
        [ ((variavel1, variavel2), correlacao), ... ]
    """

    logging.info(f"Extraindo as {limite} maiores correlações...")
    try:
        corr = correlacao.copy().abs()
        pares = []  
        colunas = corr.columns

        for i in range(len(colunas)):
            for j in range(i + 1, len(colunas)):
                pares.append(((colunas[i], colunas[j]), corr.iloc[i, j]))
        
        pares_ordenados = sorted(pares, key=lambda x: x[1], reverse=True)
        resultado = pares_ordenados[:limite]
    
    except Exception:
        logging.error("Erro ao extrair maiores correlações.", exc_info=True)
        raise

    return resultado


def calcular_vif(df: pd.DataFrame, images_dir: str) -> pd.DataFrame:
    """
    Calcula o Fator de Inflação da Variância (VIF) para todas as variáveis
    preditoras numéricas, excluindo as variáveis-alvo.

    O VIF indica multicolinearidade:
        - VIF > 5 sugere correlação forte
        - VIF > 10 indica multicolinearidade severa

    Parâmetros:
        df (DataFrame): dados já tratados e renomeados.
        images_dir (str): caminho onde o CSV com a tabela VIF será salvo.

    Retorna:
        DataFrame com as variáveis e seus respectivos VIFs.
    """
    logging.info("Calculando VIF (Variance Inflation Factor)...")
     
    try:
        # Selecionar variáveis numéricas
        col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

        # Excluir variaveis alvo
        preditoras = [
            c for c in col_numericas 
            if c not in["Carga_Aquecimento", "Carga_Resfriamento"]
        ]

        if len(preditoras) == 0:
            logging.error("Nenhuma variável preditora encontrada para cálculo de VIF.")
            raise ValueError("Dataset vazio ou colunas inorretas.")

        # Criar matriz apenas com preditoras
        x = df[preditoras]

        # DataFrame para resultado
        vif_dados = pd.DataFrame()
        vif_dados["Variavel"] = preditoras
        vif_dados["VIF"] = [
            variance_inflation_factor(x.values, i) 
            for i in range(len(preditoras))
        ]

    except Exception:
        logging.error("Erro ao calcular VIF.", exc_info=True)
        raise

    # Salvar arquivo CSV
    try:
        caminho_csv = os.path.join(images_dir, "vif_tabela.csv")
        vif_dados.to_csv(caminho_csv, index=False)
        logging.info(f"Tabela VIF salva em: {caminho_csv}")

    except Exception:
        logging.error("Erro ao salvar arquivo CSV de VIF.", exc_info=True)
        raise
    
    return vif_dados


def scatterplots_aqueciemneto(df: pd.DataFrame, images_dir: str) -> None:
    """
    Gera scatterplots entre a variável alvo 'Carga_Aquecimento' e todas as 
    demais variáveis preditoras numéricas.

    Cada gráfico é salvo como PNG no diretório especificado.

    Parâmetros:
        df (DataFrame): conjunto de dados.
        images_dir (str): diretório onde as imagens serão salvas.

    Retorna:
        None
    """
    target = "Carga_Aquecimento"
    logging.info(f"Gerando scatterplots para: {target}")

    try:
        # Selecionar somente variaveis numéricas
        col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclir variavel alvo
        preditoras = [
            col for col in col_numericas 
            if col not in ["Carga_Aquecimento", "Carga_Resfriamento"]
        ]
    except Exception:
        logging.error("Erro ao identificar variáveis numéricas para scatterplots.", exc_info=True)
        raise

    # Geração de Grafico
    for coluna in preditoras:

        try:
            plt.figure(figsize=(6,4))
            sns.scatterplot(x=df[coluna], y=df[target])
            plt.title(f"{coluna} vs {target}")
            plt.xlabel(coluna)
            plt.ylabel(target)
                
            caminho = os.path.join(images_dir, f"scatter_{target}_{coluna}.png")
                
            plt.tight_layout()
            plt.savefig(caminho)
            plt.close()
        
        except Exception:
            logging.error(f"Erro ao gerar scatterplot para a coluna: {coluna}", exc_info=True)
            raise
    
    logging.info("Scatterplots de aquecimento gerados com sucesso.")



def scatterplots_refriamento(df: pd.DataFrame, images_dir: str) -> None:
    """
    Gera scatterplots entre a variável alvo 'Carga_Resfriamento' e todas as 
    variáveis preditoras numéricas.
    
    Cada gráfico é salvo como PNG no diretório informado.

    Parâmetros:
        df (DataFrame): conjunto de dados já tratado.
        images_dir (str): diretório onde as imagens serão salvas.

    Retorno:
        None
    """
    target = "Carga_Resfriamento"
    logging.info(f"Gerando scatterplots para: {target}")

    try:
        # Selecionar variáveis numéricas
        col_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

        # Remover as duas variáveis-alvo para obter apenas preditoras
        preditores = [
            col for col in col_numericas 
            if col not in ["Carga_Aquecimento", "Carga_Resfriamento"]
        ]
    except Exception:
        logging.error("Erro ao selecionar as variáveis preditoras.", exc_info=True)
        raise

    # Geração dos gráficos    
    for coluna in preditores:
            
        try:    
            plt.figure(figsize=(6,4))
            sns.scatterplot(x=df[coluna], y=df[target])
            plt.title(f"Scatterplot de {coluna} vs {target}")
            plt.xlabel(coluna)
            plt.ylabel(target)

            caminho = os.path.join(images_dir, f"scatter_{target}_{coluna}.png")
            plt.tight_layout()
            plt.savefig(caminho)
            plt.close()
        except Exception:
            logging.error(f"Erro ao gerar scatterplot da coluna {coluna}", exc_info=True)
            raise

    logging.info("Scatterplots de resfriamento gerados com sucesso.")
    


def gerar_relatorio_pdf(
        df: pd.DataFrame, 
        descricao: pd.DataFrame, 
        nulos: pd.Series, 
        correlacao: pd.DataFrame, 
        maiores_correlacoes: list,
        info_texto: str,
        paths: dict
    ) -> None:
    """
    Gera o relatório completo da Análise Exploratória (AT1) em PDF.

    O relatório contém:
        - Capa
        - Tabela 1: df.info()
        - Sumário Executivo
        - Tabela 2: Estatísticas Descritivas (describe)
        - Tabela de valores nulos
        - Maiores correlações
        - Heatmap de correlação
        - Histogramas
        - Boxplots
        - Scatterplots (aquecimento e resfriamento)
        - Tabela VIF
    """

    logging.info("Gerando relatório PDF completo da EDA...")



    images_dir = paths["IMAGES_DIR"]
    pdf_path = paths["PDF_PATH"]
   
    largura, altura = A4
    c = canvas.Canvas(pdf_path, pagesize=A4)


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

    linhas_info = info_texto.split("\n")
    y = altura - 90

    for linha in linhas_info:
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
    c.drawString(40, altura - 126,"As próximas seções detalham os achados da análise exploratória.")
    c.showPage()


   # ---------- DESCRIBE ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Tabela 2: Estatísticas Descritivas")

    c.setFont("Courier", 8)
    linhas_desc = descricao.T.to_string().split("\n")
    y = altura - 90

    for linha in linhas_desc:
        c.drawString(40, y, linha)
        y -= 10
        
         # quebra de página automática
        if y < 60:
            c.showPage()
            c.setFont("Courier", 8)
            y = altura - 60
    
    c.showPage()


    # ---------- VALORES NULOS ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 60, "Valores Nulos por Coluna")
    
    c.setFont("Helvetica", 11)
    y = altura - 90

    for col, val in nulos.items():
        c.drawString(40, y, f"- {col}: {val}")
        y -= 14
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = altura - 60
    
    c.showPage()


    # ---------- MAIORES CORRELAÇÕES ----------
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
    caminho_heat = os.path.join(images_dir, "heatmap_correlacao.png")
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
    hist_images = {
        f for f in os.listdir(images_dir)
        if f.startswith("hist_")
        
    }

    for fname in hist_images:
        caminho_img = os.path.join(images_dir, fname)
        if not os.path.exists(caminho_img):
            continue
            
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, altura - 60, f"Figura: {fname}")
        
        img = ImageReader(caminho_img)
        iw, ih = img.getSize()
        img_w = largura - 80
        img_h = img_w * (ih / iw)
        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)



    # ---------- BOXPLOTS ----------
    imagens_box = [
        f for f in os.listdir(images_dir)
        if f.startswith("box_")
    ]

    for fname in imagens_box:
        caminho_img = os.path.join(images_dir, fname)
        if not os.path.exists(caminho_img):
            continue
            
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, altura - 60, f"Figura: {fname}")
        
        img = ImageReader(caminho_img)
        iw, ih = img.getSize()
        img_w = largura - 80
        img_h = img_w * (ih / iw)
        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)


    # ---------- SCATTERPLOTS AQUECIMENTO ----------
    imagens_scatter_aq = [
        f for f in os.listdir(images_dir)
        if f.startswith("scatter_Carga_Aquecimento")
    ]
    
    for fname in imagens_scatter_aq:
        caminho_img = os.path.join(images_dir, fname)
        if not os.path.exists(caminho_img):
            continue
            
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, altura - 60, f"Figura: {fname}")

        img = ImageReader(caminho_img)
        iw, ih = img.getSize()
        img_w = largura - 80
        img_h = img_w * (ih / iw)
        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)

    # ---------- SCATTERPLOTS RESFRIAMENTO ----------
    imagens_scatter_res = [
        f for f in os.listdir(images_dir)
        if f.startswith("scatter_Carga_Resfriamento")
    ]
    
    for fname in imagens_scatter_res:
        caminho_img = os.path.join(images_dir, fname)
        if not os.path.exists(caminho_img):
            continue

        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, altura - 60, f"Figura: {fname}")
        img = ImageReader(caminho_img)

        iw, ih = img.getSize()
        img_w = largura - 80
        img_h = img_w * (ih / iw)
        c.drawImage(img, 40, altura - 100 - img_h, width=img_w, height=img_h)


    # ---------- VIF ----------
    caminho_vif = os.path.join(images_dir, "vif_tabela.csv")

    if os.path.exists(caminho_vif):
        vif_df = pd.read_csv(caminho_vif)

        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, altura - 60, "Tabela 3: Fator de Inflação da Variância (VIF)")
        
        c.setFont("Courier", 9)
        y = altura - 90

        linhas_vif = vif_df.to_string(index=False).split("\n")
        for linha in linhas_vif:
            c.drawString(40, y, linha)
            y -= 12
            if y < 60:
                c.showPage()
                c.setFont("Courier", 9)
                y = altura - 60

    c.save()
    logging.info(f"Relatório PDF salvo em: {pdf_path}")


def executar_analise_exploratoria(paths: dict) -> None:
    """
    Executa todo o pipeline da Análise Exploratória.
    Esta função deve ser chamada pelo main.py.
    """
    logging.info("Executando pipeline da Análise Exploratória...")

    # 1. Ler dados (CSV já convertido)
    df = ler_arquivo_csv(paths["DATA_PATH"])

    # 2. Renomear colunas
    df = renomear_colunas_pt_br(df)

    # 3. Info como texto
    info_texto = info(df)

    # 4. Estatísticas descritivas
    descricao = estatisticas_descritivas(df)

    # 5. Valores nulos
    nulos = verificar_nulos(df)

    # 6. Gráficos principais
    gerar_histogramas(df, paths["IMAGES_DIR"])
    correl = gerar_matriz_correlacao(df, paths["IMAGES_DIR"])

    # 7. Scatterplots
    scatterplots_aqueciemneto(df, paths["IMAGES_DIR"])
    scatterplots_refriamento(df, paths["IMAGES_DIR"])

    # 8. Maiores correlações
    maiores = extrair_maiores_correlacoes(correl, limite=6)

    # 9. VIF
    calcular_vif(df, paths["IMAGES_DIR"])

    # 10. Gerar PDF
    gerar_relatorio_pdf(
        df=df,
        descricao=descricao,
        nulos=nulos,
        correlacao=correl,
        maiores_correlacoes=maiores,
        info_texto=info_texto,
        paths=paths
    )

    logging.info("Pipeline da AT1 concluído com sucesso.")
