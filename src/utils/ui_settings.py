import gradio as gr


class UISettings:
    @staticmethod
    def feedback(data: gr.LikeData):
        if data.liked:
            print("Você votou positivamente nesta resposta: " + data.value)
        else:
            print("Você votou negativamente nesta resposta: " + data.value)
