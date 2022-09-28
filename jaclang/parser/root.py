from typing import Optional

from jaclang.generator import Instruction, NopInstruction, ImmediatePcInstruction, JmpInstruction, PushInstruction, \
    ImmediateLabelInstruction, ADDR_REG, GetSpInstruction, SB_REG
from jaclang.lexer import Token, EndToken
from jaclang.parser.branch import Branch, BranchFactory, SymbolData
from jaclang.parser.stack_manager import StackManager


class RootBranch(Branch):
    def __init__(self, branches: list[Branch]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        for branch in self.branches:
            branch.printInfo(nested_level)

    def generateInstructions(self, symbols: dict[str, SymbolData], _: Optional[StackManager] = None) -> list[Instruction]:
        instructions = []
        for branch in self.branches:
            instructions += branch.generateInstructions(symbols)

        jump_instructions: list[Instruction] = [
            PushInstruction(ADDR_REG),
            ImmediateLabelInstruction(ADDR_REG, "fmain"),
            JmpInstruction(ADDR_REG),
        ]

        jump_size = 0
        for instruction in jump_instructions:
            jump_size += instruction.length

        start_instructions: list[Instruction] = [
            GetSpInstruction(SB_REG),
            ImmediatePcInstruction(ADDR_REG, jump_size + 4),
        ]

        start_instructions += jump_instructions + [
            NopInstruction(),
        ]
        return start_instructions + instructions


class RootFactory(BranchFactory):
    factories = []

    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        branches = []
        while tokens[pos] != EndToken():
            for factory in RootFactory.factories:
                pos, branch = factory.parseExpect(pos, tokens)
                branches.append(branch)

        return pos, RootBranch(branches)
