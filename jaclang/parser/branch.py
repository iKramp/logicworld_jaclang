from abc import abstractmethod

from jaclang.lexer import Token


class Branch:
    @abstractmethod
    def parse(self, pos: int, tokens: list[Token]) -> int:
        pass

    def printInfo(self, nested_level: int):
        pass
