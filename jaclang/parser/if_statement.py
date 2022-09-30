from typing import Optional

from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser import IdManager
from jaclang.parser.root import SymbolData
from jaclang.parser.scope import ScopeFactory, BranchInScope, BranchInScopeFactory
from jaclang.parser.stack_manager import StackManager


class IfStatementBranch(BranchInScope):
    def __init__(self):
        pass

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        return []

    def printInfo(self, nested_level: int):
        pass


class IfStatementFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        return pos, IfStatementBranch()


ScopeFactory.factories.append(IfStatementFactory())
