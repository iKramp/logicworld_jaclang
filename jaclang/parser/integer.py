from typing import Optional

from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, ConstantToken
from jaclang.parser.branch import BranchFactory, Branch, TokenExpectedException, SymbolData
from jaclang.parser.expression import ValueBranch, ValueFactory
from jaclang.parser.id_manager import IdManager
from jaclang.parser.stack_manager import StackManager


class IntegerBranch(ValueBranch):
    def __init__(self, value: int):
        self.value = value

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, self.value)

    def generateInstructions(self, symbols: dict[str, SymbolData],  id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        return [Instructions.Immediate(Registers.RETURN, self.value)]


class IntegerFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if type(tokens[pos]) is not ConstantToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected integer")
        value = tokens[pos].value
        pos += 1
        return pos, IntegerBranch(value)


ValueFactory.factories.append(IntegerFactory())
