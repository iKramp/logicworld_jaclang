from abc import abstractmethod
from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction
from jaclang.lexer import Token, Symbols, EndToken
from jaclang.parser.id_manager import IdManager
from jaclang.parser.root import SymbolData
from jaclang.parser.stack_manager import StackManager


class BranchInScope:
    @abstractmethod
    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: StackManager) -> list[Instruction]:
        pass

    @abstractmethod
    def printInfo(self, nested_level: int):
        pass


class BranchInScopeFactory:
    @abstractmethod
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        pass

    def parseExpect(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        try:
            return self.parseImpl(pos, tokens)
        except TokenExpectedException as exception:
            raise TokenNeededException(exception.pos, exception.message)

    def parseDontExpect(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
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


class ScopeBranch(BranchInScope):
    def __init__(self, branches: list[BranchInScope]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "scope:")
        for branch in self.branches:
            branch.printInfo(nested_level + 1)

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []
        for branch in self.branches:
            instructions += branch.generateInstructions(symbols, id_manager, stack_manager)
        return instructions


class ScopeFactory(BranchInScopeFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if pos >= len(tokens) or tokens[pos] != Symbols.LEFT_BRACE:
            raise TokenExpectedException(tokens[pos].pos, "Expected '{' at beginning of scope")
        pos += 1

        branches = []
        while tokens[pos] != Symbols.RIGHT_BRACE:
            recognized = False
            for factory in ScopeFactory.factories:
                pos, branch = factory.parseDontExpect(pos, tokens)
                if branch is not None:
                    branches.append(branch)
                    recognized = True
            if tokens[pos] == EndToken():
                raise TokenNeededException(tokens[pos].pos, "Expected '}' at the end of scope")
            if not recognized:
                raise TokenNeededException(tokens[pos].pos, "Did not recognize statement")
        pos += 1

        return pos, ScopeBranch(branches)


ScopeFactory.factories.append(ScopeFactory())
