from openai import OpenAI

from commons.utils import prompt_path
from scripts.components import OpenAIBot, DEFAULT_WELCOME_MESSAGE, DEFAULT_EXIT_MESSAGE
from scripts.io.terminal import TerminalIO


class TerminalBot:
    exit_codes = ["done", "quit", "exit"]

    client = OpenAI()
    prompt = prompt_path(file_name="financial_bot.txt")
    input_output = TerminalIO("User: ", "Agent: ")

    openai_bot = OpenAIBot(client, "gpt-4o-mini", prompt, 10, exit_codes=exit_codes)

    def start(self):
        self.input_output.output(DEFAULT_WELCOME_MESSAGE)
        while True:
            user_input = self.input_output.input()
            response = self.openai_bot.respond(user_input)
            if not response:
                break
            self.input_output.output(response)

        self.input_output.output(DEFAULT_EXIT_MESSAGE)

