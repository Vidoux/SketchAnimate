# !/usr/bin/env python3
import argparse
import os

import antlr4

from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.executor.SketchAnimateExecutor import SketchAnimateExecutor


from src.language.visitors.SketchAnimateChecker import SketchAnimateChecker

def execute_script(file_path):
    os.chdir(os.path.dirname(os.path.abspath(file_path)))

    # Lecture du fichier
    input_stream = antlr4.FileStream(file_path, encoding='utf-8')

    # Lexer et Parser
    lexer = SketchAnimateImperativeParadigmLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = SketchAnimateImperativeParadigmParser(token_stream)

    tree = parser.program()

    # Vérification
    checker = SketchAnimateChecker()
    try:
        checker.visit(tree)
    finally:
        checker.reportErrors()

    executor = SketchAnimateExecutor()
    executor.visit(tree)
    executor.execute_actions()
    print("Script exécuté avec succès.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécutez un script SketchAnimate (.ska).")

    help_txt="Usage: sketchanimate [OPTIONS] SCRIPT_PATH\
    Executes a SketchAnimate script (.ska), animating SVG elements based on the instructions defined within the .ska file. The script allows for complex animations including movement, rotation, color change, and visibility adjustments of SVG elements.\
    Arguments:\
    SCRIPT_PATH  Path to the SketchAnimate script (.ska) to be executed. The path can be absolute or relative to the current directory.\n\
    Options:\
    -h, --help  Show this message and exit.\
    Examples:\
  sketchanimate animations/myscript.ska  Execute the 'myscript.ska' located in the 'animations' directory.\
    For more information and documentation, visit https://github.com/Vidoux/SketchAnimate."

    parser.add_argument("script_path", help=help_txt)
    args = parser.parse_args()

    execute_script(args.script_path)
