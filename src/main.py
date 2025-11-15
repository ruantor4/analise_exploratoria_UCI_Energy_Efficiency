from convert_csv import converter_excel_para_csv
from analise_exploratoria import (
    ler_arquivo_csv,
    renomear_colunas_pt_br,
    estatisticas_descritivas,
    info,
    verificar_nulos,
    gerar_histogramas,
    gerar_matriz_correlacao,
    extrair_maiores_correlacoes,
    scatterplots_aqueciemneto,
    scatterplots_refriamento,
    calcular_vif,
    gerar_relatorio_pdf,
    DATA_PATH
)

def main():
    #converte arquivo para csv
    converter_excel_para_csv()
    # Ler dados
    df = ler_arquivo_csv(DATA_PATH)

    # Renomear colunas
    df = renomear_colunas_pt_br(df)

    # Info
    info(df)

    # Estatísticas descritivas
    descricao = estatisticas_descritivas(df)

    # Nulos
    nulos = verificar_nulos(df)

    # Gráficos principais
    gerar_histogramas(df)
    correl = gerar_matriz_correlacao(df)

    # Scatterplots
    scatterplots_aqueciemneto(df)
    scatterplots_refriamento(df)

    # Correlações fortes
    maiores = extrair_maiores_correlacoes(correl, limite=6)

    # VIF
    calcular_vif(df)

    # PDF final
    gerar_relatorio_pdf(df, descricao, nulos, correl, maiores)

if __name__ == "__main__":
    main()