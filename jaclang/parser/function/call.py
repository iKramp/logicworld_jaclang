from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, IdentifierToken, Symbols
from jaclang.parser.expression import ValueBranch
from jaclang.parser.function.declaration import FunctionData
from jaclang.parser.scope import BranchInScope, BranchInScopeFactory, TokenExpectedException, TokenNeededException, \
    ScopeContext


class FunctionCallBranch(ValueBranch):
    def __init__(self, function_name: str):
        self.function_name = function_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"call: {self.function_name}()")

    def generateInstructions(self, context: ScopeContext) -> list[Instruction]:
        if self.function_name not in context.symbols.keys():
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' undefined")

        if type(context.symbols[self.function_name]) is not FunctionData:
            raise JaclangSyntaxError(-1, f"Symbol '{self.function_name}' is not a function")

        jmp_label = f"jmp{context.id_manager.requestId()}"
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
