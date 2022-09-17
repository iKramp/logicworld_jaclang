from jaclang.lexer import Token
from jaclang.parser.branch import Branch


class FunctionDeclarationBranch(Branch):
    def parse(self, pos: int, tokens: list[Token]) -> int:
        pass

    def printInfo(self, nested_level: int):
        pass
