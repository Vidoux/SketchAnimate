from antlr4 import FileStream, CommonTokenStream

from tests.language.ErrorListenerTest import ErrorListenerTest
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.executor.SketchAnimateExecutor import SketchAnimateExecutor

# Create Lexer and Parser
input_stream = FileStream("JO_script.ska", encoding='utf-8')
lexer = SketchAnimateImperativeParadigmLexer(input_stream)
token_stream = CommonTokenStream(lexer)
print(token_stream.getText())
parser = SketchAnimateImperativeParadigmParser(token_stream)
parser.addErrorListener(ErrorListenerTest())
tree = parser.program()

executor = SketchAnimateExecutor()
executor.visit(tree)
executor.execute_actions()
print("Traitement terminé")