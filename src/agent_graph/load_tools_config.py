import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

load_dotenv()

# Prints para testar a conexão ao banco
# print(f"POSTGRES_DB_HOST: {os.getenv('POSTGRES_DB_HOST')}")
# print(f"POSTGRES_DB_PORT: {os.getenv('POSTGRES_DB_PORT')}")
# print(f"POSTGRES_DB_NAME: {os.getenv('POSTGRES_DB_NAME')}")
# print(f"POSTGRES_DB_USER: {os.getenv('POSTGRES_DB_USER')}")
# print(f"POSTGRES_DB_PASSWORD: {os.getenv('POSTGRES_DB_PASSWORD')}")


class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("configs/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Definir variáveis ​​de ambiente
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")

        # Agente primário
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Configuração de pesquisa na Internet
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])
              
        # Configurações PostgreSQL agent
        self.postgres_db_host = os.getenv("POSTGRES_DB_HOST", app_config["postgres_sqlagent_configs"]["db_host"])
        self.postgres_db_port = os.getenv("POSTGRES_DB_PORT", app_config["postgres_sqlagent_configs"]["db_port"])
        self.postgres_db_name = os.getenv("POSTGRES_DB_NAME", app_config["postgres_sqlagent_configs"]["db_name"])
        self.postgres_db_user = os.getenv("POSTGRES_DB_USER", app_config["postgres_sqlagent_configs"]["db_user"])
        self.postgres_db_password = os.getenv("POSTGRES_DB_PASSWORD", app_config["postgres_sqlagent_configs"]["db_password"])

        self.postgres_sqlagent_llm = app_config["postgres_sqlagent_configs"]["llm"]
        self.postgres_sqlagent_llm_temperature = float(app_config["postgres_sqlagent_configs"]["llm_temperature"])


        # Configurações Graph
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])
