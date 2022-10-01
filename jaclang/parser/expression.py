from __future__ import annotations

from abc import ABC, abstractmethod

from jaclang.generator import Instruction, Instructions, CompareFlags, Registers
from jaclang.lexer import Token, Symbols
from jaclang.parser.scope import ScopeFactory, BranchInScope, BranchInScopeFactory, TokenExpectedException, ScopeContext


class Operator:
    operators = {}

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generateInstructions(self) -> list[Instruction]:
        pass


class PlusOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Add(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class MinusOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Subtract(Registers.RETURN, Registers.EXPRESSION, Registers.RETURN)]


class EqualsOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.EQUAL)]


class LesserOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.LESSER)]


class GreaterOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.GREATER)]


class LesserOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.LESSER_OR_EQUAL)]


class GreaterOrEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.GREATER_OR_EQUAL)]


class NotEqualOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Compare(Registers.EXPRESSION, Registers.RETURN, CompareFlags.NOT_EQUAL)]


class BitShiftLeftOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.BitShiftLeft(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class BitShiftRightOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.BitShiftRight(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class OrOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Or(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class XorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Xor(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class AndOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.And(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class XnorOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Xnor(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


class NandOperator(Operator):
    def generateInstructions(self) -> list[Instruction]:
        return [Instructions.Nand(Registers.EXPRESSION, Registers.RETURN, Registers.RETURN)]


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


class ValueBranch(BranchInScope, ABC):
    pass


class ValueFactory(BranchInScopeFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
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

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        instructions = []

        instructions += self.value1.generateInstructions(context)
        instructions += [
            Instructions.Mov(Registers.RETURN, Registers.EXPRESSION),
            Instructions.Push(Registers.EXPRESSION),
        ]
        instructions += self.value2.generateInstructions(context)
        instructions += [
            Instructions.Pop(Registers.EXPRESSION),
        ]

        instructions += self.expr_operator.generateInstructions()

        return instructions


class ExpressionFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
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


class ParenthesesFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1

        expr_factory = ExpressionFactory()
        pos, expr = expr_factory.parseExpect(pos, tokens)

        if tokens[pos] != Symbols.RIGHT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected ')'")

        pos += 1

        return pos, expr


def load():
    ScopeFactory.factories.append(ExpressionFactory())
    ValueFactory.factories.append(ParenthesesFactory())
