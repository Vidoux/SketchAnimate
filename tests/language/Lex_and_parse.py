import sys
from antlr4 import FileStream, CommonTokenStream

import tests.language.ErrorListenerTest
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from SketchAnimateExecutor import SketchAnimateExecutor

# Create Lexer and Parser
input_stream = FileStream("example2_Imperative.ska")
lexer = SketchAnimateImperativeParadigmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = SketchAnimateImperativeParadigmParser(token_stream)
parser.addErrorListener(tests.language.ErrorListenerTest.ErrorListenerTest())
tree = parser.program()  # 'program' is root rule

executor = SketchAnimateExecutor()
executor.visit(tree)

