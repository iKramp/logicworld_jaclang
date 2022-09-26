from __future__ import annotations

from abc import ABC
from typing import Optional

from jaclang.generator import Instruction, PushInstruction, EXPR_REG, PopInstruction, AddInstruction, RET_REG, \
    SubInstruction, MovInstruction
from jaclang.lexer import Token, PLUS, MINUS, SymbolToken, UNKNOWN
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException
from jaclang.parser.scope import ScopeFactory
from jaclang.parser.stack_manager import StackManager


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
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        for factory in ValueFactory.factories:
            pos, value = factory.parseDontExpect(pos, tokens)
            if value is not None:
                return pos, value

        raise TokenExpectedException(tokens[pos].pos, "Expected value")


class ExpressionBranch(Branch):
    def __init__(self, branch: Optional[ExpressionBranch], expr_operator: Operator, value: ValueBranch):
        self.branch = branch
        self.value = value
        self.expr_operator = expr_operator

    def printInfoRecursive(self, nested_level: int):
        if self.expr_operator != NO_OPERATOR:
            self.branch.printInfoRecursive(nested_level)
            print('    ' * nested_level, self.expr_operator.name)
        self.value.printInfo(nested_level)
    
    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "Expression:")
        self.printInfoRecursive(nested_level + 1)

    def generateInstructions(self, stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = [
            PushInstruction(EXPR_REG),
        ]

        instructions += self.generateInstructionsRecursively(stack_manager)

        instructions += [
            PopInstruction(EXPR_REG),
        ]
        return instructions

    def generateInstructionsRecursively(self, stack_manager: StackManager) -> list[Instruction]:
        if self.expr_operator == NO_OPERATOR:
            return self.value.generateInstructions(stack_manager) + [MovInstruction(RET_REG, EXPR_REG)]

        instructions = self.branch.generateInstructionsRecursively(stack_manager)
        instructions += self.value.generateInstructions(stack_manager)
        if self.expr_operator == PLUS_OPERATOR:
            instructions += [
                AddInstruction(EXPR_REG, RET_REG, EXPR_REG),
            ]
        elif self.expr_operator == MINUS_OPERATOR:
            instructions += [
                SubInstruction(EXPR_REG, RET_REG, EXPR_REG),
            ]
        return instructions


class ExpressionFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        value_factory = ValueFactory()
        pos, value = value_factory.parseDontExpect(pos, tokens)
        if value is None:
            raise TokenExpectedException(tokens[pos].pos, "Expected value")

        return self.parseRecursive(pos, tokens, ExpressionBranch(None, NO_OPERATOR, value))

    def parseRecursive(self, pos: int, tokens: list[Token], expr_branch: ExpressionBranch) -> (int, ExpressionBranch):
        if tokens[pos] not in Operator.operators.keys():
            return pos, expr_branch

        expr_operator = Operator.operators[tokens[pos]]
        pos += 1
        value_factory = ValueFactory()
        pos, value = value_factory.parseDontExpect(pos, tokens)
        new_expr_branch = ExpressionBranch(expr_branch, expr_operator, value)

        return self.parseRecursive(pos, tokens, new_expr_branch)


ScopeFactory.factories.append(ExpressionFactory())
