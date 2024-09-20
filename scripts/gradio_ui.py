from pathlib import Path

import gradio as gr

from commons.loggerfactory import LoggerFactory
from scripts.components import OpenAIBot, DEFAULT_WELCOME_MESSAGE, DEFAULT_EXIT_MESSAGE, ChatHistory


GREETING_PROMPT = ("You con imagine a story hook and imagine the state of Rick.\n"
                   "You see Morty, Greet him in few words!")
EXIT_PROMPT = "Morty is leaving. Give an apt response. Keep it short"


class GradioBotUI:
    def __init__(self, bot: OpenAIBot, user_avatar: str | Path, agent_avatar: str | Path):
        self.logger = LoggerFactory.getLogger(self.__class__.__name__)
        self.bot = bot
        self.user_avatar = user_avatar
        self.agent_avatar = agent_avatar

    def launch(self):
        self.logger.info("Launching gradio ui ...")
        with gr.Blocks(title="Rick and Morty!", fill_height=True) as demo:
            with gr.Row():
                gr.Image(value="media/rnm_title.png", height="100px", container=False, show_download_button=False,
                         show_fullscreen_button=False)

            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        gr.HTML(value="<center><h1>Adventure generator</h1></center>")
                    with gr.Row():
                        gr.Image(value="media/rnm_poster.png", container=False, show_download_button=False,
                                 show_fullscreen_button=False, height="80%")

                with gr.Column():
                    history = self.bot.get_history_copy()
                    greetings = self.greeting(history)
                    with gr.Row():
                        chatbot = gr.Chatbot(bubble_full_width=False, show_copy_button=True,
                                             avatar_images=(self.user_avatar, self.agent_avatar), scale=1,
                                             value=[[None, greetings]], show_copy_all_button=True)

                    with gr.Row():
                        prompt = gr.Textbox(label="Prompt")
                    state = gr.State(value=history)

            user_step = prompt.submit(self.user_message, inputs=[prompt, chatbot],
                                      outputs=[prompt, chatbot], queue=False)
            user_step.then(self.agent_message, inputs=[state, chatbot], outputs=[prompt, state, chatbot])

        demo.launch(server_port=8080, server_name="0.0.0.0")
        self.logger.info("Done launching gradio ui!")

    def user_message(self, user_text, history):
        return gr.Textbox(label="Prompt"), history + [[user_text, None]]

    def greeting(self, chat_history: ChatHistory):
        response = self.bot.respond(GREETING_PROMPT, chat_history, append_user_input=True)
        return response

    def __bye(self, chat_history: ChatHistory):
        response = self.bot.respond(EXIT_PROMPT, chat_history, append_user_input=False)
        return response

    def agent_message(self, chat_history: ChatHistory, history):
        user_text = history[-1][0]
        response = self.bot.respond(user_text, chat_history)
        if not response:
            history[-1][1] = self.__bye(chat_history)
            return gr.Textbox(label="Prompt", interactive=False), chat_history, history
        history[-1][1] = response
        return "", chat_history, history
