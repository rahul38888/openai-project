import os.path
import pathlib
from pathlib import Path

from openai import OpenAI

from scripts.components import OpenAIBot
from scripts.io.terminal import TerminalIO

exit_codes = ["done", "quit", "exit"]

client = OpenAI()
prompt = pathlib.Path(__file__).parent.resolve() / "system_prompts" / "financial_bot.txt"
input_output = TerminalIO("User: ", "Agent: ")

openai_bot = OpenAIBot(client, "gpt-4o-mini", prompt, 10, input_output,
                       exit_codes=exit_codes)

if __name__ == '__main__':
    openai_bot.start()
    while openai_bot.interact():
        pass


