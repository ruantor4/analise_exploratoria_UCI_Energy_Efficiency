import os
import pandas as pd

PATH_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATH_XLSX = os.path.join(PATH_BASE, "data", "ENB2012_data.xlsx")
PATH_CSV = os.path.join(PATH_BASE, "data", "dados.csv")

def converter_excel_para_csv():
    """
        Converte o arquivo ENB2012_data.xlsx para dados.csv.
        Executado apenas se o CSV não existir.
    """
    if os.path.exists(PATH_CSV):
        print("CSV já existe. Pulando conversão...")
        return

    print(f"Lendo arquivo Excel: {PATH_XLSX}")
    df = pd.read_excel(PATH_XLSX)

    print(f"Salvando CSV em: {PATH_CSV}")
    df.to_csv(PATH_CSV, index=False, encoding="utf-8")

    print("Conversão concluída com sucesso!")