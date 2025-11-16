import logging
import os
from convert_csv import converter_excel_para_csv
from analise_exploratoria import executar_analise_exploratoria


def log_system(log_path: str):
    """
    Configura o sistema de logs da aplicação.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers={
            logging.FileHandler(log_path, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        }
    )
    logging.info("======== INÍCIO DA EXECUÇÃO ========")
    


def main():

    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    PATHS = {
        # Caminhos
        "BASE_PATH": BASE_PATH,
        "DATA_XLSX": os.path.join(BASE_PATH, "data", "ENB2012_data.xlsx"),
        "DATA_PATH": os.path.join(BASE_PATH, "data","dados.csv"),
        "OUTPUTS_DIR": os.path.join(BASE_PATH, "outputs"),
        "IMAGES_DIR": os.path.join(BASE_PATH,"outputs", "figs"),
        "lOG_PATH": os.path.join(BASE_PATH, "outputs", "logs"),
        "PDF_PATH": os.path.join(BASE_PATH,"outputs", "relatorio_analise.pdf"),   
    }
    
    # Criar pastas de saída caso não existam
    os.makedirs(PATHS["OUTPUTS_DIR"], exist_ok=True)
    os.makedirs(PATHS["IMAGES_DIR"], exist_ok=True)
    
    # Configurar Logs
    log_system(PATHS["lOG_PATH"])


    try:
       logging.info("Convertendo Excel para CSV....")
       converter_excel_para_csv(PATHS["DATA_XLSX"], PATHS["DATA_PATH"])
       executar_analise_exploratoria(PATHS)

    except Exception as e:
        logging.error("ERRO CRÍTICO DURANTE A EXECUÇÃO")

if __name__ == "__main__":
    main()