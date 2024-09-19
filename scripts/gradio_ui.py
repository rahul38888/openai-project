from pathlib import Path

import gradio as gr

from commons.loggerfactory import LoggerFactory
from scripts.components import OpenAIBot, DEFAULT_WELCOME_MESSAGE, DEFAULT_EXIT_MESSAGE, ChatHistory


class GradioBotUI:
    def __init__(self, bot: OpenAIBot, user_avatar: str | Path, agent_avatar: str | Path):
        self.logger = LoggerFactory.getLogger(self.__class__.__name__)
        self.bot = bot
        self.user_avatar = user_avatar
        self.agent_avatar = agent_avatar

    def launch(self):
        self.logger.info("Launching gradio ui ...")
        with gr.Blocks(title="Butter Robot!", fill_height=True) as demo:
            with gr.Row():
                gr.Markdown(
                    """
                    <center>
                        <h1>Butter Robot!</h1>
                        <h3>What is my purpose? </h3>
                    </center>
                    """)

            with gr.Column():
                chatbot = gr.Chatbot(bubble_full_width=False, likeable=True, show_copy_button=True,
                                     avatar_images=(self.user_avatar, self.agent_avatar),
                                     value=[[None, DEFAULT_WELCOME_MESSAGE]], scale=1)
                prompt = gr.Textbox(label="Prompt")
                state = gr.State(value=(self.bot.get_history_copy()))

            user_step = prompt.submit(self.user_message, inputs=[prompt, chatbot],
                                      outputs=[prompt, chatbot], queue=False)
            user_step.then(self.agent_message, inputs=[state, chatbot], outputs=[prompt, state, chatbot])

        demo.launch(server_port=8080, server_name="0.0.0.0")
        self.logger.info("Done launching gradio ui!")

    def user_message(self, user_text, history):
        return gr.Textbox(label="Prompt"), history + [[user_text, None]]

    def agent_message(self, chat_history: ChatHistory, history):
        user_text = history[-1][0]
        response = self.bot.respond(user_text, chat_history)
        if not response:
            history[-1][1] = DEFAULT_EXIT_MESSAGE
            return gr.Textbox(label="Prompt", interactive=False), chat_history, history
        history[-1][1] = response
        return "", chat_history, history
