import logging
import os
import pandas as pd

def converter_excel_para_csv(xlsx_path, csv_path: str) -> None:
    """
    Converte o arquivo XLSX para CSV.
    Se o CSV já existir, ele será substituído automaticamente.
    """
    try:
        logging.info(f"Lendo arquivo Excel: {xlsx_path}")
        df = pd.read_excel(xlsx_path)

        # Cria pastas se faltar
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        logging.info(f"Salvando CSV em: {csv_path}")
        df.to_csv(csv_path, index=False)

        logging.info("Conversão para CSV concluída com sucesso.")

    except FileNotFoundError:
        logging.error("Arquivo XLSX não encontrado.", exc_info=True)
        raise

    except Exception:
        logging.error("Erro ao converter Excel para CSV.", exc_info=True)
        raise
    