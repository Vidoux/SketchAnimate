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

    def test_main_sequence(self):
        self.run_test_file('test_main_sequence.ska')

    def test_sequence_params(self):
        self.run_test_file('test_sequence_params.ska')

    def test_sequence_nesting(self):
        self.run_test_file('test_sequence_nesting.ska')

    def test_sequence_declaration(self):
        self.run_test_file('test_sequence_declaration.ska')

    def test_sequence_error(self):
        self.run_test_file('test_sequence_error.ska', expected_errors=1)


if __name__ == '__main__':
    unittest.main()
