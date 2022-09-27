from typing import Optional

from jaclang.generator import Instruction, LabelInstruction, RetInstruction, PushInstruction, SB_REG, PopInstruction, \
    GetSpInstruction
from jaclang.lexer import Token, IdentifierToken, LEFT_BRACKET, RIGHT_BRACKET, FUNC_KEYWORD
from jaclang.parser import RootFactory
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException, SymbolData
from jaclang.parser.expression import ValueFactory, ValueBranch
from jaclang.parser.scope import ScopeFactory, ScopeBranch
from jaclang.parser.stack_manager import StackManager


class FunctionDeclarationBranch(Branch):
    def __init__(self, name: str, body: ScopeBranch):
        self.name = name
        self.body = body

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self, symbols: dict[str, SymbolData], _: Optional[StackManager] = None) -> list[Instruction]:
        stack_manager = StackManager()
        body_instructions = self.body.generateInstructions(stack_manager)

        begin_instructions: list[Instruction] = [
            LabelInstruction("f" + self.name),
            PushInstruction(SB_REG),
            GetSpInstruction(SB_REG),
        ]

        end_instructions: list[Instruction] = [
            PopInstruction(SB_REG),
            RetInstruction(),
        ]

        return begin_instructions + body_instructions + end_instructions


class FunctionDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != FUNC_KEYWORD:
            raise TokenExpectedException(tokens[pos].pos, "Expected func keyword in function declaration")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected identifier after func keyword")
        func_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != LEFT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected '(' after func name")

        pos += 1
        if tokens[pos] != RIGHT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected ')' after '('")

        pos += 1

        pos, body = ScopeFactory().parseExpect(pos, tokens)

        return pos, FunctionDeclarationBranch(func_name, body)


class FunctionCallBranch(ValueBranch):
    def __init__(self, function_name: str):
        self.function_name = function_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"call: {self.function_name}()")

    def generateInstructions(self, symbols: dict[str, SymbolData], _: Optional[StackManager] = None) -> list[Instruction]:
        return []


class FunctionCallFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        function_name = tokens[pos].identifier
        pos += 1
        if tokens[pos] != LEFT_BRACKET:
            raise TokenExpectedException(tokens[pos].pos, "Expected '('")

        pos += 1
        if tokens[pos] != RIGHT_BRACKET:
            raise TokenNeededException(tokens[pos].pos, "Expected ')'")

        pos += 1
        return pos, FunctionCallBranch(function_name)


ValueFactory.factories.append(FunctionCallFactory())
RootFactory.factories.append(FunctionDeclarationFactory())
