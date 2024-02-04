import antlr4
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser

from src.language.visitors.SketchAnimateChecker import SketchAnimateChecker
from src.language.listeners.SketchAnimateErrorListener import SketchAnimateErrorListener


def main():
    # Chemin vers le fichier de test
    file_path = './test_full_features.ska'

    # Lecture du fichier de test
    input_stream = antlr4.FileStream(file_path, encoding='utf-8')

    # Création du Lexer et du Parser
    lexer = SketchAnimateImperativeParadigmLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = SketchAnimateImperativeParadigmParser(token_stream)

    # Personnalised error listener
    error_listener = SketchAnimateErrorListener()
    parser.removeErrorListeners()  # Remove predefined error listener
    parser.addErrorListener(error_listener)

    tree = parser.program()

    # Création et utilisation du Checkeur
    checker = SketchAnimateChecker()
    try:
        checker.visit(tree)
    finally:
        checker.reportErrors()


if __name__ == "__main__":
    main()
