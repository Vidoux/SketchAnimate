import unittest
from antlr4 import FileStream, CommonTokenStream
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser


class TestSketchAnimateLexerParser(unittest.TestCase):

    def run_test_file(self, file_path, expected_errors=0):
        input_stream = FileStream(file_path)
        lexer = SketchAnimateImperativeParadigmLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SketchAnimateImperativeParadigmParser(stream)
        parser.program()
        self.assertEqual(parser.getNumberOfSyntaxErrors(), expected_errors, f"Syntax errors found in {file_path}")

    def test_create_group(self):
        self.run_test_file('test_create_group.ska')

    def test_move_to(self):
        self.run_test_file('test_move_to.ska')

    def test_rotate(self):
        self.run_test_file('test_rotate.ska')

    def test_change_color(self):
        self.run_test_file('test_change_color.ska')

    def test_syntax_error(self):
        self.run_test_file('test_syntax_error.ska', expected_errors=1)


if __name__ == '__main__':
    unittest.main()
