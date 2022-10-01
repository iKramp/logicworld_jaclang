from abc import abstractmethod

from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, EndToken
from jaclang.parser.id_manager import IdManager


class SymbolData:
    pass


class RootContext:
    def __init__(self, symbols: dict[str, SymbolData], id_manager: IdManager):
        self.symbols = symbols
        self.id_manager = id_manager


class BranchInRoot:
    @abstractmethod
    def generateInstructions(self, context: RootContext) -> list[Instruction]:
        pass

    @abstractmethod
    def printInfo(self, nested_level: int):
        pass


class BranchInRootFactory:
    @abstractmethod
    def parse(self, pos: int, tokens: list[Token]) -> (int, BranchInRoot):
        pass


class RootBranch:
    def __init__(self, branches: list[BranchInRoot]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        for branch in self.branches:
            branch.printInfo(nested_level)

    def generateInstructions(self) -> list[Instruction]:
        instructions = []

        context = RootContext({}, IdManager())
        for branch in self.branches:
            instructions += branch.generateInstructions(context)

        start_instructions: list[Instruction] = [
            Instructions.GetStackPointer(Registers.STACK_BASE),
            Instructions.ImmediateLabel(Registers.ADDRESS, "end_program"),
            Instructions.Push(Registers.ADDRESS),
            Instructions.ImmediateLabel(Registers.ADDRESS, "fmain"),
            Instructions.Jump(Registers.ADDRESS),
            Instructions.Label("end_program"),
            Instructions.Terminate(),
        ]

        return start_instructions + instructions


class RootFactory:
    factories = []

    @staticmethod
    def parse(pos: int, tokens: list[Token]) -> (int, RootBranch):
        branches = []
        while tokens[pos] != EndToken():
            for factory in RootFactory.factories:
                pos, branch = factory.parse(pos, tokens)
                branches.append(branch)

        return pos, RootBranch(branches)
