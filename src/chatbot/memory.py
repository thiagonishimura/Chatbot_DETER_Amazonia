import os
import pandas as pd
from typing import List
from datetime import datetime, date


class Memory:
    @staticmethod
    def write_chat_history_to_file(gradio_chatbot: List,  thread_id: str, folder_path: str) -> None:
        tmp_list = list(gradio_chatbot[-1])  # Converta a tupla em uma lista

        today_str = date.today().strftime('%Y-%m-%d')
        tmp_list.insert(0, thread_id)  # Adiciona um novo valor à lista

        current_time_str = datetime.now().strftime('%H:%M:%S')
        tmp_list.insert(1, current_time_str)  # Adiciona um novo valor à lista

        # Caminho do arquivo CSV de hoje
        file_path = os.path.join(folder_path, f'{today_str}.csv')

        # Crie um DataFrame da lista
        new_df = pd.DataFrame([tmp_list], columns=[
                              "thread_id", "timestamp", "user_query", "response"])

        # Verifique se o arquivo de hoje existe
        if os.path.exists(file_path):
            # Se existir, anexe os novos dados ao arquivo CSV
            new_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # Caso não exista, crie o arquivo CSV com os novos dados
            new_df.to_csv(file_path, mode='w', header=True, index=False)
