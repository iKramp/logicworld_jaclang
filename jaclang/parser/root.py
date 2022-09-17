from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser import FunctionDeclarationBranch
from jaclang.parser.branch import Branch, BranchFactory
from jaclang.parser.function import FunctionDeclarationFactory


class RootBranch(Branch):
    def __init__(self, functions: list[FunctionDeclarationBranch]):
        self.functions = functions

    def printInfo(self, nested_level: int):
        for function in self.functions:
            function.printInfo(nested_level)

    def generateInstructions(self) -> list[Instruction]:
        return []


class RootFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        function_factory = FunctionDeclarationFactory()
        functions = []
        while pos < len(tokens):
            pos, function = function_factory.parseExpect(pos, tokens)
            functions.append(function)

        return pos, RootBranch(functions)
