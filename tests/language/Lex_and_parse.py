import sys
from antlr4 import FileStream, CommonTokenStream

from tests.language.ErrorListenerTest import ErrorListenerTest
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from SketchAnimateExecutor import SketchAnimateExecutor

# Create Lexer and Parser
input_stream = FileStream("example2_Imperative.ska")
lexer = SketchAnimateImperativeParadigmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
print(token_stream.getText())
parser = SketchAnimateImperativeParadigmParser(token_stream)
parser.addErrorListener(ErrorListenerTest())
tree = parser.program()  # 'program' is root rule

executor = SketchAnimateExecutor()
executor.visit(tree)


executor.finalize_animation("final_animation.gif")
print("end ")