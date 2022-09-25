from typing import Optional

from jaclang.generator.generator import Instruction
from jaclang.lexer import Token, VAR_KEYWORD, IdentifierToken, ASSIGNMENT
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException
from jaclang.parser.expression import ExpressionBranch, ExpressionFactory, ValueFactory, ValueBranch
from jaclang.parser.scope import ScopeFactory


class VariableDeclarationBranch(Branch):
    def __init__(self, variable_name: str, value: Optional[ExpressionBranch]):
        self.variable_name = variable_name
        self.value = value

    def generateInstructions(self) -> list[Instruction]:
        return []

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "VariableDeclaration:")
        print('    ' * nested_level, f"    name: {self.variable_name}")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class VariableDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != VAR_KEYWORD:
            raise TokenExpectedException(tokens[pos].pos, "Expected var keyword")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] == ASSIGNMENT:
            pos += 1
            expression_factory = ExpressionFactory()
            pos, value = expression_factory.parseExpect(pos, tokens)
            return pos, VariableDeclarationBranch(variable_name, value)
        else:
            return pos, VariableDeclarationBranch(variable_name, None)


class VariableBranch(ValueBranch):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"var: {self.variable_name}")

    def generateInstructions(self) -> list[Instruction]:
        return []


class VariableFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        variable_name = tokens[pos].identifier
        pos += 1
        return pos, VariableBranch(variable_name)


ValueFactory.factories.append(VariableFactory())
ScopeFactory.factories.append(VariableDeclarationFactory())
