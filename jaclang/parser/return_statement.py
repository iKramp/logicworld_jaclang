from typing import Optional

from jaclang.generator import Instruction, RetInstruction, MovInstruction, EXPR_REG, RET_REG
from jaclang.lexer import Token, RETURN_KEYWORD
from jaclang.parser.branch import Branch, BranchFactory, SymbolData, TokenExpectedException
from jaclang.parser.expression import ExpressionBranch, ExpressionFactory
from jaclang.parser.scope import ScopeFactory
from jaclang.parser.stack_manager import StackManager


class ReturnStatementBranch(Branch):
    def __init__(self, value: Optional[ExpressionBranch]):
        self.value = value

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(symbols, stack_manager)
        instructions += [
            RetInstruction(),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "return:")
        self.value.printInfo(nested_level + 1)


class ReturnStatementFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != RETURN_KEYWORD:
            raise TokenExpectedException(pos, "Expected return keyword")

        pos += 1

        expression_factory = ExpressionFactory()
        pos, value_branch = expression_factory.parseDontExpect(pos, tokens)

        return pos, ReturnStatementBranch(value_branch)


ScopeFactory.factories.append(ReturnStatementFactory())
