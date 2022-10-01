from copy import copy
from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, IdentifierToken, Symbols, Keywords
from jaclang.parser.root import RootFactory
from jaclang.parser.expression import ValueFactory, ValueBranch, ExpressionBranch, ExpressionFactory
from jaclang.parser.id_manager import IdManager
from jaclang.parser.root import SymbolData, BranchInRoot, BranchInRootFactory
from jaclang.parser.scope import ScopeFactory, ScopeBranch, BranchInScope, BranchInScopeFactory, TokenExpectedException, \
    TokenNeededException
from jaclang.parser.stack_manager import StackManager


class FunctionData(SymbolData):
    pass


class ReturnStatementBranch(BranchInScope):
    def __init__(self, value: Optional[ExpressionBranch]):
        self.value = value

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> \
            list[Instruction]:
        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(symbols, id_manager, stack_manager)
        instructions += [
            Instructions.Pop(Registers.ADDRESS),
            Instructions.SetStackPointer(Registers.STACK_BASE),
            Instructions.Mov(Registers.ADDRESS, Registers.STACK_BASE),
            Instructions.Pop(Registers.ADDRESS),
            Instructions.Jump(Registers.ADDRESS),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "return:")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class ReturnStatementFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScopeFactory):
        if tokens[pos] != Keywords.RETURN:
            raise TokenExpectedException(pos, "Expected return keyword")

        pos += 1

        expression_factory = ExpressionFactory()
        pos, value_branch = expression_factory.parseDontExpect(pos, tokens)

        return pos, ReturnStatementBranch(value_branch)


class FunctionDeclarationBranch(BranchInRoot):
    def __init__(self, name: str, body: ScopeBranch):
        self.name = name
        self.body = body

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager) -> list[Instruction]:
        symbols[self.name] = FunctionData()

        stack_manager = StackManager()
        func_symbols = copy(symbols)
        body_instructions = self.body.generateInstructions(func_symbols, id_manager, stack_manager)

        begin_instructions: list[Instruction] = [
            Instructions.Label("f" + self.name),
            Instructions.Mov(Registers.STACK_BASE, Registers.ADDRESS),
            Instructions.GetStackPointer(Registers.STACK_BASE),
            Instructions.Immediate(Registers.RETURN, stack_manager.getSize()),
            Instructions.Add(Registers.STACK_BASE, Registers.RETURN, Registers.RETURN),
            Instructions.SetStackPointer(Registers.RETURN),
            Instructions.Push(Registers.ADDRESS),
        ]

        return begin_instructions + body_instructions


class FunctionDeclarationFactory(BranchInRootFactory):
    def parse(self, pos: int, tokens: list[Token]) -> (int, BranchInRoot):
        if tokens[pos] != Keywords.FUNC:
            raise TokenExpectedException(tokens[pos].pos, "Expected func keyword in function declaration")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected identifier after func keyword")
        func_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected '(' after func name")

        pos += 1
        if tokens[pos] != Symbols.RIGHT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected ')' after '('")

        pos += 1

        pos, body = ScopeFactory().parseExpect(pos, tokens)
        body.branches.append(ReturnStatementBranch(None))

        return pos, FunctionDeclarationBranch(func_name, body)


class FunctionCallBranch(ValueBranch):
    def __init__(self, function_name: str):
        self.function_name = function_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"call: {self.function_name}()")

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, _: Optional[StackManager] = None) -> list[Instruction]:
        if self.function_name not in symbols.keys():
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' undefined")

        if type(symbols[self.function_name]) is not FunctionData:
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' is not a function")

        jmp_label = f"jmp{id_manager.requestId()}"
        start_instructions: list[Instruction] = [
            Instructions.ImmediateLabel(Registers.ADDRESS, jmp_label),
            Instructions.Push(Registers.ADDRESS),
            Instructions.ImmediateLabel(Registers.ADDRESS, "f" + self.function_name),
            Instructions.Jump(Registers.ADDRESS),
            Instructions.Label(jmp_label),
        ]
        return start_instructions


class FunctionCallFactory(BranchInScopeFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, BranchInScope):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        function_name = tokens[pos].identifier
        pos += 1
        if tokens[pos] != Symbols.LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1
        if tokens[pos] != Symbols.RIGHT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected ')'")

        pos += 1
        return pos, FunctionCallBranch(function_name)


def load():
    ValueFactory.factories.append(FunctionCallFactory())
    RootFactory.factories.append(FunctionDeclarationFactory())
    ScopeFactory.factories.append(ReturnStatementFactory())
