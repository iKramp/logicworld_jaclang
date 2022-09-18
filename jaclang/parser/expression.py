from __future__ import annotations

from abc import ABC

from jaclang.generator import Instruction
from jaclang.lexer import Token, PLUS, MINUS
from jaclang.parser.branch import Branch, BranchFactory

operators = [PLUS, MINUS]


class ValueBranch(Branch, ABC):
    pass


class ExpressionBranch(Branch):
    def __init__(self, value: ValueBranch, operator, next_branch: ExpressionBranch):
        self.value = value
        self.operator = operator
        self.next_branch = next_branch

    def printInfo(self, nested_level: int):
        pass

    def generateInstructions(self) -> list[Instruction]:
        return []


class ValueFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        pass


class ExpressionFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        pass
