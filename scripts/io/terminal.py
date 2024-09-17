from scripts.io import InputOutput


class TerminalIO(InputOutput):

    def __init__(self, input_prompt: str, output_prompt: str):
        self.__input_prompt = input_prompt
        self.__output_prompt = output_prompt

    def input(self) -> str:
        return input(self.__input_prompt)

    def output(self, message: str):
        print(f"{self.__output_prompt} {message}")

