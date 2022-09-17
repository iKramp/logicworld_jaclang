from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser.branch import Branch, BranchFactory


class FunctionDeclarationBranch(Branch):
    def printInfo(self, nested_level: int):
        pass

    def generateInstructions(self) -> list[Instruction]:
        pass


class FunctionDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        return pos + 1, None
