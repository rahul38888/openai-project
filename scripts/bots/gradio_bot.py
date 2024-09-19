from openai import OpenAI

from commons.utils import prompt_path, media_path
from scripts.components import OpenAIBot
from scripts.gradio_ui import GradioBotUI
from scripts.io.terminal import TerminalIO


class GradioBot:
    exit_codes = ["done", "quit", "exit"]

    client = OpenAI()
    prompt = prompt_path(file_name="financial_bot.txt")
    input_output = TerminalIO("User: ", "Agent: ")

    openai_bot = OpenAIBot(client, "gpt-4o-mini", prompt, 10, exit_codes=exit_codes)

    gradio_bot = GradioBotUI(openai_bot, user_avatar=media_path("user.png"), agent_avatar=media_path("agent.png"))

    def start(self):
        self.gradio_bot.launch()
