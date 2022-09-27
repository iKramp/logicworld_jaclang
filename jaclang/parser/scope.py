from typing import Optional

from jaclang.generator import Instruction
from jaclang.lexer import Token, LEFT_BRACE, RIGHT_BRACE, EndToken
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException, SymbolData
from jaclang.parser.stack_manager import StackManager


class ScopeBranch(Branch):
    def __init__(self, branches: list[Branch]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "scope:")
        for branch in self.branches:
            branch.printInfo(nested_level + 1)

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []
        for branch in self.branches:
            instructions += branch.generateInstructions(symbols, stack_manager)
        return instructions


class ScopeFactory(BranchFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if pos >= len(tokens) or tokens[pos] != LEFT_BRACE:
            raise TokenExpectedException(tokens[pos].pos, "Expected '{' at beginning of scope")
        pos += 1

        branches = []
        while tokens[pos] != RIGHT_BRACE:
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
