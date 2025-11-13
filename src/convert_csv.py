import os
import pandas as pd

PATH_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATH_XLSX = os.path.join(PATH_BASE, "data", "ENB2012_data.xlsx")
PATH_CSV = os.path.join(PATH_BASE, "data", "dados.csv")


print(f"Lendo arquivo Excel: {PATH_XLSX}")
df = pd.read_excel(PATH_XLSX)


print(f"Salvando CSV em: {PATH_CSV}")
df.to_csv(PATH_CSV, index=False, encoding="utf-8")


print("Conversão concluída com sucesso!")