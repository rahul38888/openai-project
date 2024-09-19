from openai import OpenAI

from commons.loggerfactory import LoggerFactory
from commons.utils import prompt_path, media_path
from scripts.components import OpenAIBot
from scripts.gradio_ui import GradioBotUI
from scripts.io.terminal import TerminalIO


class GradioBot:
    exit_codes = ["done", "quit", "exit"]

    client = OpenAI()
    prompts = [prompt_path(file_name="rick_and_morty/System_prompt.txt")]

    openai_bot = OpenAIBot(client, "gpt-4o-mini", prompts, 30, exit_codes=exit_codes)

    gradio_bot = GradioBotUI(openai_bot, user_avatar=media_path("characters/morty.png"),
                             agent_avatar=media_path("characters/rick.png"))

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self.__class__.__name__)

    def start(self):
        self.logger.info("Starting gradio bot ...")
        self.gradio_bot.launch()
