from typing import List, Tuple
import os
import psycopg2
from chatbot.load_config import LoadProjectConfig
from agent_graph.load_tools_config import LoadToolsConfig
from agent_graph.build_full_graph import build_graph
from utils.app_utils import create_directory
from chatbot.memory import Memory
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from tabulate import tabulate
from flask import Flask, render_template_string
import threading

PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()
graph = build_graph()
config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}
create_directory("memory")

app = Flask(__name__)

@app.route('/table')
def table():
    return render_template_string(app.config['table_html'])

class ChatBot:

    @staticmethod
    def respond(chatbot: List, message: str) -> Tuple:
        try:
            # Configurar o modelo LLM
            llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            # Definir o prompt para classificar a mensagem
            classification_prompt = PromptTemplate(
                input_variables=["message"],
                template=(
                    "Classifique a seguinte mensagem como 'pergunta' ou 'consulta'. "
                    "Uma 'pergunta' é uma questão geral que não requer acesso ao banco de dados. "
                    "Uma 'consulta' é uma solicitação que requer acesso ao banco de dados para obter informações específicas. "
                    "Mensagem: {message}"
                )
            )

            # Criar a cadeia LLM para classificação
            classification_chain = classification_prompt | llm

            # Classificar a mensagem
            classification = classification_chain.invoke(message).strip().lower()
            print(f"Classificação da mensagem: {classification}")

            if classification == "pergunta":
                # Responder a pergunta normal
                response_prompt = PromptTemplate(
                    input_variables=["message"],
                    template="Responda a seguinte pergunta: {message}"
                )
                response_chain = response_prompt | llm
                response = response_chain.invoke(message)
                chatbot.append((message, response))
            elif classification == "consulta":
                # Definir o prompt para gerar a consulta SQL
                query_prompt = PromptTemplate(
                    input_variables=["message"],
                    template="Gere uma consulta SQL para a seguinte mensagem: {message}"
                )
                query_chain = query_prompt | llm

                # Gerar a consulta SQL
                query = query_chain.invoke(message)
                print(f"Consulta gerada: {query}")

                # Conectar ao banco de dados
                # Conectar ao banco de dados
                connection = psycopg2.connect(
                    host=os.getenv("POSTGRES_DB_HOST"),
                    database=os.getenv("POSTGRES_DB_NAME"),
                    user=os.getenv("POSTGRES_DB_USER"),
                    password=os.getenv("POSTGRES_DB_PASSWORD")
                )
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                connection.close()

                # Processar e retornar o resultado
                if "tabelas" in message.lower() or "colunas" in message.lower():
                    formatted_result = '\n'.join([row[0] for row in result])
                else:
                    formatted_result = tabulate(result, headers=columns, tablefmt="html")
                    threading.Thread(target=ChatBot.display_table, args=(formatted_result,)).start()
                
                chatbot.append((message, formatted_result))
            else:
                print(f"Classificação inesperada: {classification}")
                raise Exception("Classificação inválida da mensagem.")

        except Exception as e:
            error_message = f"Ocorreu um erro durante o processamento: {str(e)}. Tente novamente."
            chatbot.append((message, error_message))
            print("Erro detalhado:", e)

        Memory.write_chat_history_to_file(
            gradio_chatbot=chatbot, folder_path=PROJECT_CFG.memory_dir, thread_id=TOOLS_CFG.thread_id
        )
        return "", chatbot

    @staticmethod
    def display_table(table_html):
        app.config['table_html'] = table_html
        app.run(debug=True, use_reloader=False)
