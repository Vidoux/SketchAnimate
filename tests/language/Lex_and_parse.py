import sys
from antlr4 import FileStream, CommonTokenStream

import tests.language.ErrorListenerTest
from src.language.codegen.antlr_build.SketchAnimateObjectParadigmLexer import SketchAnimateObjectParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateObjectParadigmParser import SketchAnimateObjectParadigmParser
from SketchAnimateExecutor import SketchAnimateExecutor

# Create Lexer and Parser
input_stream = FileStream("example_parser_error_1.ska")
lexer = SketchAnimateObjectParadigmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = SketchAnimateObjectParadigmParser(token_stream)
parser.addErrorListener(tests.language.ErrorListenerTest.ErrorListenerTest())
tree = parser.program()  # 'program' is root rule

executor = SketchAnimateExecutor()
executor.visit(tree)

