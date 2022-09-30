from copy import copy
from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, LabelInstruction, PushInstruction, SB_REG, PopInstruction, \
    GetSpInstruction, ADDR_REG, JmpInstruction, ImmediateLabelInstruction, MovInstruction, \
    ImmediateInstruction, RET_REG, AddInstruction, SetSpInstruction
from jaclang.lexer import Token, IdentifierToken, Symbols, Keywords
from jaclang.parser import RootFactory
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException, SymbolData
from jaclang.parser.expression import ValueFactory, ValueBranch, ExpressionBranch, ExpressionFactory
from jaclang.parser.id_manager import IdManager
from jaclang.parser.scope import ScopeFactory, ScopeBranch
from jaclang.parser.stack_manager import StackManager


class FunctionData(SymbolData):
    pass


class ReturnStatementBranch(Branch):
    def __init__(self, value: Optional[ExpressionBranch]):
        self.value = value

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, stack_manager: Optional[StackManager] = None) -> \
            list[Instruction]:
        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(symbols, id_manager, stack_manager)
        instructions += [
            PopInstruction(ADDR_REG),
            SetSpInstruction(SB_REG),
            MovInstruction(ADDR_REG, SB_REG),
            PopInstruction(ADDR_REG),
            JmpInstruction(ADDR_REG),
        ]
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "return:")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class ReturnStatementFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != Keywords.RETURN:
            raise TokenExpectedException(pos, "Expected return keyword")

        pos += 1

        expression_factory = ExpressionFactory()
        pos, value_branch = expression_factory.parseDontExpect(pos, tokens)

        return pos, ReturnStatementBranch(value_branch)


class FunctionDeclarationBranch(Branch):
    def __init__(self, name: str, body: ScopeBranch):
        self.name = name
        self.body = body

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self, symbols: dict[str, SymbolData], id_manager: IdManager, _: Optional[StackManager] = None) -> list[Instruction]:
        symbols[self.name] = FunctionData()

        stack_manager = StackManager()
        func_symbols = copy(symbols)
        body_instructions = self.body.generateInstructions(func_symbols, id_manager, stack_manager)

        begin_instructions: list[Instruction] = [
            LabelInstruction("f" + self.name),
            MovInstruction(SB_REG, ADDR_REG),
            GetSpInstruction(SB_REG),
            ImmediateInstruction(RET_REG, stack_manager.getSize()),
            AddInstruction(SB_REG, RET_REG, RET_REG),
            SetSpInstruction(RET_REG),
            PushInstruction(ADDR_REG),
        ]

        return begin_instructions + body_instructions


class FunctionDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
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
            ImmediateLabelInstruction(ADDR_REG, jmp_label),
            PushInstruction(ADDR_REG),
            ImmediateLabelInstruction(ADDR_REG, "f" + self.function_name),
            JmpInstruction(ADDR_REG),
            LabelInstruction(jmp_label),
        ]
        return start_instructions


class FunctionCallFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
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


ValueFactory.factories.append(FunctionCallFactory())
RootFactory.factories.append(FunctionDeclarationFactory())
ScopeFactory.factories.append(ReturnStatementFactory())
