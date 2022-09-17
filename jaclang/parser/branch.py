from abc import abstractmethod

from jaclang.generator import Instruction
from jaclang.lexer import Token


class Branch:
    @abstractmethod
    def generateInstructions(self) -> list[Instruction]:
        pass

    @abstractmethod
    def printInfo(self, nested_level: int):
        pass


class BranchFactory:
    @abstractmethod
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        pass

    def parseExpect(self, pos: int, tokens: list[Token]) -> (int, Branch):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as exception:
            raise TokenNeededException(exception)

    def parseDontExpect(self, pos: int, tokens: list[Token]) -> (int, Branch):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as _:
            raise (pos, None)


# Parser did not recognize branch type (throws if you need to have a branch present somewhere)
class TokenExpectedException(Exception):
    pass


# Parser has already recognized branch type and spotted a syntax error
class TokenNeededException(Exception):
    pass
