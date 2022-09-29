from typing import Optional

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, MemwInstruction, RET_REG, SB_REG, MemrInstruction
from jaclang.lexer import Token, VAR_KEYWORD, IdentifierToken, ASSIGNMENT
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException, SymbolData
from jaclang.parser.expression import ExpressionBranch, ExpressionFactory, ValueFactory, ValueBranch
from jaclang.parser.scope import ScopeFactory
from jaclang.parser.stack_manager import StackManager


class VariableData(SymbolData):
    def __init__(self, pos_on_stack: int):
        self.pos_on_stack = pos_on_stack


class VariableAssignmentBranch(Branch):
    def __init__(self, variable_name: str, value: Optional[ExpressionBranch]):
        self.variable_name = variable_name
        self.value = value

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        if self.variable_name not in symbols.keys():
            raise JaclangSyntaxError(-1, f"Variable '{self.variable_name}' not found")
        variable_obj = symbols[self.variable_name]
        if type(variable_obj) is not VariableData:
            raise JaclangSyntaxError(-1, f"Label '{self.variable_name}' is not a variable")

        instructions = []
        if self.value is not None:
            instructions += self.value.generateInstructions(symbols, stack_manager)
            instructions += [
                MemwInstruction(SB_REG, variable_obj.pos_on_stack, RET_REG),
            ]
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "VariableAssignment:")
        print('    ' * nested_level, f"    name: {self.variable_name}")
        if self.value is not None:
            self.value.printInfo(nested_level + 1)


class VariableAssignmentFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] != ASSIGNMENT:
            raise TokenExpectedException(tokens[pos].pos, "Expected '='")
        pos += 1
        expression_factory = ExpressionFactory()
        pos, value = expression_factory.parseExpect(pos, tokens)
        return pos, VariableAssignmentBranch(variable_name, value)


class VariableDeclarationBranch(Branch):
    def __init__(self, variable_name: str, value: Optional[ValueBranch]):
        self.variable_name = variable_name
        self.assignment = VariableAssignmentBranch(variable_name, value)

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        pos_on_stack = stack_manager.allocate()
        symbols[self.variable_name] = VariableData(pos_on_stack)

        instructions = []
        if self.assignment is not None:
            instructions += self.assignment.generateInstructions(symbols, stack_manager)
        return instructions

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "VariableDeclaration:")
        print('    ' * nested_level, f"    name: {self.variable_name}")
        if self.assignment is not None:
            self.assignment.value.printInfo(nested_level + 1)


class VariableDeclarationFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if tokens[pos] != VAR_KEYWORD:
            raise TokenExpectedException(tokens[pos].pos, "Expected var keyword")

        pos += 1
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenNeededException(tokens[pos].pos, "Expected variable name after var keyword")
        variable_name = tokens[pos].identifier

        pos += 1
        if tokens[pos] == ASSIGNMENT:
            pos += 1
            expression_factory = ExpressionFactory()
            pos, value = expression_factory.parseExpect(pos, tokens)
            return pos, VariableDeclarationBranch(variable_name, value)
        else:
            return pos, VariableDeclarationBranch(variable_name, None)


class VariableBranch(ValueBranch):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, f"var: {self.variable_name}")

    def generateInstructions(self, symbols: dict[str, SymbolData], stack_manager: Optional[StackManager] = None) -> list[Instruction]:
        if self.variable_name not in symbols.keys():
            raise JaclangSyntaxError(-1, f"Variable '{self.variable_name}' not found")
        variable_obj = symbols[self.variable_name]
        if type(variable_obj) is not VariableData:
            raise JaclangSyntaxError(-1, f"Label '{self.variable_name}' is not a variable")

        return [
            MemrInstruction(SB_REG, variable_obj.pos_on_stack, RET_REG),
        ]


class VariableFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        if type(tokens[pos]) is not IdentifierToken:
            raise TokenExpectedException(tokens[pos].pos, "Expected identifier")
        variable_name = tokens[pos].identifier
        pos += 1
        return pos, VariableBranch(variable_name)


ValueFactory.factories.append(VariableFactory())
ScopeFactory.factories.append(VariableDeclarationFactory())
ScopeFactory.factories.append(VariableAssignmentFactory())
