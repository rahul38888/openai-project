from abc import ABC, abstractmethod


class InputOutput(ABC):

    @abstractmethod
    def input(self) -> str:
        ...

    @abstractmethod
    def output(self, message: str):
        ...
