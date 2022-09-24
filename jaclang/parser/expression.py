from __future__ import annotations

from abc import ABC

from jaclang.generator import Instruction
from jaclang.lexer import Token, PLUS, MINUS, SymbolToken, UNKNOWN
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException
from jaclang.parser.scope import ScopeFactory


class Operator:
    operators = {}

    def __init__(self, name: str, token: SymbolToken):
        self.name = name
        Operator.operators[token] = self


NO_OPERATOR = Operator("", UNKNOWN)
PLUS_OPERATOR = Operator("+", PLUS)
MINUS_OPERATOR = Operator("-", MINUS)


class ValueBranch(Branch, ABC):
    pass


class ValueFactory(BranchFactory):
    factories = set()

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        for factory in ValueFactory.factories:
            pos, value = factory.parseDontExpect(pos, tokens)
            if value is not None:
                return pos, value

        raise TokenExpectedException(tokens[pos].pos, "Expected value")


class ExpressionBranch(Branch):
    def __init__(self, value: ValueBranch, expr_operator: Operator, next_branch: ExpressionBranch):
        self.value = value
        self.expr_operator = expr_operator
        self.next_branch = next_branch

    def printInfoRecursive(self, nested_level: int):
        self.value.printInfo(nested_level)
        if self.expr_operator != NO_OPERATOR:
            print('    ' * nested_level, self.expr_operator.name)
            self.next_branch.printInfoRecursive(nested_level)
    
    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "Expression:")
        self.printInfoRecursive(nested_level + 1)

    def generateInstructions(self) -> list[Instruction]:
        pass


class ExpressionFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        value_factory = ValueFactory()
        pos, value = value_factory.parseDontExpect(pos, tokens)
        if value is None:
            raise TokenExpectedException(tokens[pos].pos, "Expected value")

        if tokens[pos] not in Operator.operators.keys():
            expr_operator = NO_OPERATOR
            next_branch = None
        else:
            expr_operator = Operator.operators[tokens[pos]]
            pos += 1
            branch_factory = ExpressionFactory()
            pos, next_branch = branch_factory.parseExpect(pos, tokens)

        return pos, ExpressionBranch(value, expr_operator, next_branch)


ScopeFactory.factories.add(ExpressionFactory())
