import copy
from enum import Enum
from os import PathLike

from openai import OpenAI

from commons.utils import getdefault
from scripts.io import InputOutput

DEFAULT_WELCOME_MESSAGE = "How can I assist you ..."
DEFAULT_USER_PROMPT = "User: "
DEFAULT_AGENT_PROMPT = "Agent: "
DEFAULT_EXIT_MESSAGE = "Have a nice day!"


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatHistory:
    def __init__(self, context_span: int, initial_context: list[dict[str, str]]):
        self.__context_span = context_span
        self.__context = list()
        for context in initial_context:
            self.__add_context(context)

    def __ensure_max_size(self):
        while len(self.__context) > self.__context_span:
            self.__context.pop(1)
        return self

    def __add_context(self, context: dict[str, str]) -> "ChatHistory":
        self.__context.append(context)
        return self.__ensure_max_size()

    def add_message(self, role: Role, content: str) -> "ChatHistory":
        return self.__add_context({"role": role.value, "content": content})

    def get_whole_context(self) -> list[dict[str, str]]:
        return self.__ensure_max_size().__context.copy()

    def get_chat_history(self) -> list[dict[str, str]]:
        return self.get_whole_context()[0:]

    def get_context_size(self) -> int:
        return len(self.__ensure_max_size().__context)

    def last_in_history(self):
        return self.__context[-1]

    def reset(self) -> "ChatHistory":
        self.__context.clear()
        return self


class OpenAIBot:
    def __init__(self, bot: OpenAI, model: str, prompt: PathLike | str, context_span: int, **args):
        self.__bot = bot
        self.__model = model
        final_prompt = prompt
        if isinstance(prompt, PathLike):
            with open(prompt, "r") as pf:
                final_prompt = pf.read()
        self.__history_instance = ChatHistory(context_span=context_span,
                                              initial_context=[{"role": Role.SYSTEM.value, "content": final_prompt}])
        self.__history = self.get_history_copy()
        self.__exit_codes: list = getdefault(args, "exit_codes", list())

    def __is_exit(self, message: str) -> bool:
        return message.lower() in self.__exit_codes

    def respond(self, user_input: str, history: ChatHistory = None) -> str | bool:
        if not history:
            history = self.__history

        if self.__is_exit(user_input):
            return False

        response = None
        if user_input:
            messages = history.add_message(Role.USER, user_input).get_whole_context()

            chat = self.__bot.chat.completions.create(model=self.__model, messages=messages)
            # print(f"Tokens count, prompts: {chat.usage.prompt_tokens}, completion: {chat.usage.completion_tokens}, "
            #       f"total: {chat.usage.total_tokens}")
            # del messages

            reply = chat.choices[0].message.content
            response = reply
            history.add_message(Role.ASSISTANT, reply)

        return response

    def get_history_copy(self) -> ChatHistory:
        return copy.deepcopy(self.__history_instance)
