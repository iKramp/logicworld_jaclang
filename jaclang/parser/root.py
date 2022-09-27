from typing import Optional

from jaclang.generator import Instruction, NopInstruction
from jaclang.lexer import Token, EndToken
from jaclang.parser.branch import Branch, BranchFactory, SymbolData
from jaclang.parser.stack_manager import StackManager


class RootBranch(Branch):
    def __init__(self, branches: list[Branch]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        for branch in self.branches:
            branch.printInfo(nested_level)

    def generateInstructions(self, symbols: dict[str, SymbolData], _: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []
        for branch in self.branches:
            instructions += branch.generateInstructions(symbols)
        instructions.append(NopInstruction())
        return instructions


class RootFactory(BranchFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        branches = []
        while tokens[pos] != EndToken():
            for factory in RootFactory.factories:
                pos, branch = factory.parseExpect(pos, tokens)
                branches.append(branch)

        return pos, RootBranch(branches)
