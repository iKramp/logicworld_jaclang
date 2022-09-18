from jaclang.generator import Instruction
from jaclang.lexer import Token, ConstantToken
from jaclang.parser.branch import BranchFactory, Branch, TokenExpectedException
from jaclang.parser.expression import ValueBranch, ValueFactory


class IntegerBranch(ValueBranch):
    def __init__(self, value: int):
        self.value = value

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, self.value)

    def generateInstructions(self) -> list[Instruction]:
        pass


class IntegerFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if pos >= len(tokens) or type(tokens[pos]) is not ConstantToken:
            raise TokenExpectedException("Expected integer")
        value = tokens[pos].value
        pos += 1
        return pos, IntegerBranch(value)


ValueFactory.factories.add(IntegerFactory())
