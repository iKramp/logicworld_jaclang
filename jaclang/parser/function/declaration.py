from copy import copy

from jaclang.generator import Instruction, Instructions, Registers
from jaclang.lexer import Token, Keywords, IdentifierToken, Symbols
from jaclang.parser.root import SymbolData, BranchInRoot, BranchInRootFactory, RootContext
from jaclang.parser.scope import TokenExpectedException, ScopeBranch, TokenNeededException, ScopeFactory, ScopeContext
from jaclang.parser.stack_manager import StackManager
from jaclang.parser.function.return_statement import ReturnStatementBranch


class FunctionData(SymbolData):
    pass


class FunctionDeclarationBranch(BranchInRoot):
    def __init__(self, name: str, body: ScopeBranch):
        self.name = name
        self.body = body

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"FunctionDeclaration:")
        print('    ' * nested_level, f"    name: {self.name}")
        self.body.printInfo(nested_level + 1)

    def generateInstructions(self, context: RootContext) -> list[Instruction]:
        context.symbols[self.name] = FunctionData()

        new_context = ScopeContext(copy(context.symbols), context.id_manager, StackManager())
        body_instructions = self.body.generateInstructions(new_context)

        begin_instructions: list[Instruction] = [
            Instructions.Label("f" + self.name),
            Instructions.Mov(Registers.STACK_BASE, Registers.ADDRESS),
            Instructions.GetStackPointer(Registers.STACK_BASE),
            Instructions.Immediate(Registers.RETURN, new_context.stack_manager.getSize()),
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
