from jaclang.generator.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser.branch import Branch, BranchFactory


class VariableDeclaration(Branch):
    def generateInstructions(self) -> list[Instruction]:
        pass

    def printInfo(self, nested_level: int):
        pass


class VariableDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        pass

