from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from jaclang.generator import Instruction, PushInstruction, EXPR_REG, PopInstruction, AddInstruction, RET_REG, \
    SubInstruction, MovInstruction, CmpInstruction, CMP_EQUAL, CMP_LESSER, CMP_GREATER, CMP_LESSER_OR_EQUAL, \
    CMP_GREATER_OR_EQUAL, CMP_NOT_EQUAL
from jaclang.lexer import Token, PLUS, MINUS, LEFT_BRACKET, RIGHT_BRACKET, EQUALS, LESS_THAN, GREATER_THAN, \
    LESS_OR_EQUAL_THAN, GREATER_OR_EQUAL_THAN, NOT_EQUAL
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, SymbolData
from jaclang.parser.scope import ScopeFactory
from jaclang.parser.stack_manager import StackManager


class Operator:
    operators = {}

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generateInstructions(self) -> list[Instruction]:
        pass


class PlusOperator(Operator):
    def __init__(self):
        super().__init__("+")

    def generateInstructions(self) -> list[Instruction]:
        return [AddInstruction(EXPR_REG, RET_REG, RET_REG)]


class MinusOperator(Operator):
    def __init__(self):
        super().__init__("-")

    def generateInstructions(self) -> list[Instruction]:
        return [SubInstruction(RET_REG, EXPR_REG, RET_REG)]


class EqualsOperator(Operator):
    def __init__(self):
        super().__init__("==")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_EQUAL)]


class LesserOperator(Operator):
    def __init__(self):
        super().__init__("<")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_LESSER)]


class GreaterOperator(Operator):
    def __init__(self):
        super().__init__(">")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_GREATER)]


class LesserOrEqualOperator(Operator):
    def __init__(self):
        super().__init__("<=")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_LESSER_OR_EQUAL)]


class GreaterOrEqualOperator(Operator):
    def __init__(self):
        super().__init__(">=")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_GREATER_OR_EQUAL)]


class NotEqualOperator(Operator):
    def __init__(self):
        super().__init__("!=")

    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_NOT_EQUAL)]


Operator.operators[PLUS] = PlusOperator()
Operator.operators[MINUS] = MinusOperator()
Operator.operators[EQUALS] = EqualsOperator()
Operator.operators[LESS_THAN] = LesserOperator()
Operator.operators[GREATER_THAN] = GreaterOperator()
Operator.operators[LESS_OR_EQUAL_THAN] = LesserOrEqualOperator()
Operator.operators[GREATER_OR_EQUAL_THAN] = GreaterOrEqualOperator()
Operator.operators[NOT_EQUAL] = NotEqualOperator()


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


class ExpressionBranch(ValueBranch):
    def __init__(self, value1: ValueBranch, expr_operator: Operator, value2: ValueBranch):
        self.value1 = value1
        self.value2 = value2
        self.expr_operator = expr_operator

    def printInfo(self, nested_level: int):
        self.value1.printInfo(nested_level)
        print('    ' * nested_level, self.expr_operator.name)
        self.value2.printInfo(nested_level)

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []

        instructions += self.value1.generateInstructions(symbols, stack_manager)
        instructions += [
            MovInstruction(RET_REG, EXPR_REG),
            PushInstruction(EXPR_REG),
        ]
        instructions += self.value2.generateInstructions(symbols, stack_manager)
        instructions += [
            PopInstruction(EXPR_REG),
        ]

        instructions += self.expr_operator.generateInstructions()

        return instructions


class ExpressionFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        value_factory = ValueFactory()
        pos, value = value_factory.parseDontExpect(pos, tokens)
        if value is None:
            raise TokenExpectedException(tokens[pos].pos, "Expected value")

        return self.parseRecursive(pos, tokens, value)

    def parseRecursive(self, pos: int, tokens: list[Token], expr_branch: ValueBranch) -> (int, ExpressionBranch):
        if tokens[pos] not in Operator.operators.keys():
            return pos, expr_branch

        expr_operator = Operator.operators[tokens[pos]]
        pos += 1
        value_factory = ValueFactory()
        pos, value = value_factory.parseExpect(pos, tokens)
        new_expr_branch = ExpressionBranch(expr_branch, expr_operator, value)

        return self.parseRecursive(pos, tokens, new_expr_branch)


class ParenthesesFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1

        expr_factory = ExpressionFactory()
        pos, expr = expr_factory.parseExpect(pos, tokens)

        if tokens[pos] != RIGHT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected ')'")

        pos += 1

        return pos, expr


ScopeFactory.factories.append(ExpressionFactory())
ValueFactory.factories.append(ParenthesesFactory())
