from abc import abstractmethod
from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser.stack_manager import StackManager


class SymbolData:
    pass


class Branch:
    @abstractmethod
    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
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
            raise TokenNeededException(exception.pos, exception.message)

    def parseDontExpect(self, pos: int, tokens: list[Token]) -> (int, Branch):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as _:
            return pos, None


# Parser did not recognize branch type (throws if you need to have a branch present somewhere)
class TokenExpectedException(JaclangSyntaxError):
    pass


# Parser has already recognized branch type and spotted a syntax error
class TokenNeededException(JaclangSyntaxError):
    pass
