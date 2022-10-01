from typing import Optional

from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, Keywords
from jaclang.parser import IdManager
from jaclang.parser.expression import ExpressionBranch, ExpressionFactory
from jaclang.parser.root import SymbolData
from jaclang.parser.scope import ScopeFactory, BranchInScope, BranchInScopeFactory, ModifierBranchInScope, \
    TokenExpectedException
from jaclang.parser.stack_manager import StackManager


class IfStatementBranch(ModifierBranchInScope):
    def __init__(self, condition: ExpressionBranch):
        super().__init__()
        self.condition = condition

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        instructions = self.condition.generateInstructions(symbols, id_manager, stack_manager)
        if_begin = f"if_begin:{id_manager.requestId()}"
        if_end = f"if_end:{id_manager.requestId()}"
        instructions += [
            Instructions.ImmediateLabel(Registers.ADDRESS, if_begin),
            Instructions.JumpIf(Registers.ADDRESS),
            Instructions.ImmediateLabel(Registers.ADDRESS, if_end),
            Instructions.Jump(Registers.ADDRESS),
            Instructions.Label(if_begin),
        ]
        instructions += self.branch.generateInstructions(symbols, id_manager, stack_manager)
        instructions += [
            Instructions.Label(if_end),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print("    " * nested_level, "IfStatement:")
        self.condition.printInfo(nested_level + 1)
        self.branch.printInfo(nested_level + 1)


class IfStatementFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if tokens[pos] != Keywords.IF:
            raise TokenExpectedException(tokens[pos].pos, "Expected if keyword")
        pos += 1

        expr_factory = ExpressionFactory()
        pos, condition = expr_factory.parseExpect(pos, tokens)

        return pos, IfStatementBranch(condition)


def load():
    ScopeFactory.factories.append(IfStatementFactory())
