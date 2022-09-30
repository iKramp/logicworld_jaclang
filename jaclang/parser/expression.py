from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from jaclang.generator import Instruction, PushInstruction, EXPR_REG, PopInstruction, AddInstruction, RET_REG, \
    SubInstruction, MovInstruction, CmpInstruction, CMP_EQUAL, CMP_LESSER, CMP_GREATER, CMP_LESSER_OR_EQUAL, \
    CMP_GREATER_OR_EQUAL, CMP_NOT_EQUAL, BsrInstruction, BslInstruction, OrInstruction, XorInstruction, AndInstruction, \
    XnorInstruction, NandInstruction
from jaclang.lexer import Token, Symbols
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
    def generateInstructions(self) -> list[Instruction]:
        return [AddInstruction(EXPR_REG, RET_REG, RET_REG)]


class MinusOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [SubInstruction(RET_REG, EXPR_REG, RET_REG)]


class EqualsOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_EQUAL)]


class LesserOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_LESSER)]


class GreaterOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_GREATER)]


class LesserOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_LESSER_OR_EQUAL)]


class GreaterOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_GREATER_OR_EQUAL)]


class NotEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [CmpInstruction(EXPR_REG, RET_REG, CMP_NOT_EQUAL)]


class BitShiftLeftOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [BslInstruction(EXPR_REG, RET_REG, RET_REG)]


class BitShiftRightOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [BsrInstruction(EXPR_REG, RET_REG, RET_REG)]


class OrOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [OrInstruction(EXPR_REG, RET_REG, RET_REG)]


class XorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [XorInstruction(EXPR_REG, RET_REG, RET_REG)]


class AndOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [AndInstruction(EXPR_REG, RET_REG, RET_REG)]


class XnorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [XnorInstruction(EXPR_REG, RET_REG, RET_REG)]


class NandOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [NandInstruction(EXPR_REG, RET_REG, RET_REG)]


Operator.operators[Symbols.PLUS] = PlusOperator(Symbols.PLUS.name)
Operator.operators[Symbols.MINUS] = MinusOperator(Symbols.MINUS.name)
Operator.operators[Symbols.EQUALS] = EqualsOperator(Symbols.EQUALS.name)
Operator.operators[Symbols.LESS_THAN] = LesserOperator(Symbols.LESS_THAN.name)
Operator.operators[Symbols.GREATER_THAN] = GreaterOperator(Symbols.GREATER_THAN.name)
Operator.operators[Symbols.LESS_OR_EQUAL_THAN] = LesserOrEqualOperator(Symbols.LESS_OR_EQUAL_THAN.name)
Operator.operators[Symbols.GREATER_OR_EQUAL_THAN] = GreaterOrEqualOperator(Symbols.GREATER_OR_EQUAL_THAN.name)
Operator.operators[Symbols.NOT_EQUAL] = NotEqualOperator(Symbols.NOT_EQUAL.name)
Operator.operators[Symbols.BIT_SHIFT_LEFT] = BitShiftLeftOperator(Symbols.BIT_SHIFT_LEFT.name)
Operator.operators[Symbols.BIT_SHIFT_RIGHT] = BitShiftRightOperator(Symbols.BIT_SHIFT_RIGHT.name)
Operator.operators[Symbols.OR] = OrOperator(Symbols.OR.name)
Operator.operators[Symbols.XOR] = XorOperator(Symbols.XOR.name)
Operator.operators[Symbols.AND] = AndOperator(Symbols.AND.name)
Operator.operators[Symbols.XNOR] = XnorOperator(Symbols.XNOR.name)
Operator.operators[Symbols.NAND] = NandOperator(Symbols.NAND.name)


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
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1

        expr_factory = ExpressionFactory()
        pos, expr = expr_factory.parseExpect(pos, tokens)

        if tokens[pos] != Symbols.RIGHT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected ')'")

        pos += 1

        return pos, expr


ScopeFactory.factories.append(ExpressionFactory())
ValueFactory.factories.append(ParenthesesFactory())
