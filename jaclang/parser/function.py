from jaclang.generator import Instruction
from jaclang.lexer import Token, IdentifierToken, LEFT_BRACKET, RIGHT_BRACKET, FUNC_KEYWORD
from jaclang.parser import RootFactory
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException
from jaclang.parser.scope import ScopeFactory, ScopeBranch


class FunctionDeclarationBranch(Branch):
    def __init__(self, name: str, body: ScopeBranch):
        self.name = name
        self.body = body

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self) -> list[Instruction]:
        pass


class FunctionDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != FUNC_KEYWORD:
            raise TokenExpectedException(tokens[pos].pos, "Expected func keyword in function declaration")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected identifier after func keyword")
        func_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != LEFT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected '(' after func name")

        pos += 1
        if tokens[pos] != RIGHT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected ')' after '('")

        pos += 1

        pos, body = ScopeFactory().parseExpect(pos, tokens)

        return pos, FunctionDeclarationBranch(func_name, body)


RootFactory.factories.append(FunctionDeclarationFactory())
