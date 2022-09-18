from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser.branch import Branch, BranchFactory


class RootBranch(Branch):
    def __init__(self, branches: list[Branch]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        for branches in self.branches:
            branches.printInfo(nested_level)

    def generateInstructions(self) -> list[Instruction]:
        return []


class RootFactory(BranchFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        branches = []
        while pos < len(tokens):
            for factory in RootFactory.factories:
                pos, branch = factory.parseExpect(pos, tokens)
                branches.append(branch)

        return pos, RootBranch(branches)
