from jaclang.parser import ValueFactory, RootFactory
from jaclang.parser.function.call import FunctionCallFactory
from jaclang.parser.function.declaration import FunctionDeclarationFactory
from jaclang.parser.function.return_statement import ReturnStatementFactory
from jaclang.parser.scope import ScopeFactory


def load():
    ValueFactory.factories.append(FunctionCallFactory())
    RootFactory.factories.append(FunctionDeclarationFactory())
    ScopeFactory.factories.append(ReturnStatementFactory())
