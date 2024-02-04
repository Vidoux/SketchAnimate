import unittest
from antlr4 import FileStream, CommonTokenStream
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmLexer import SketchAnimateImperativeParadigmLexer
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.visitors.SketchAnimateChecker import SketchAnimateChecker

class TestSketchAnimateChecker(unittest.TestCase):

    def run_checker(self, file_path):
        input_stream = FileStream(file_path, encoding='utf-8')
        lexer = SketchAnimateImperativeParadigmLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SketchAnimateImperativeParadigmParser(stream)
        tree = parser.program()

        checker = SketchAnimateChecker()
        checker.visit(tree)
        return checker

    def test_full_features(self):
        checker = self.run_checker('test_full_features.ska')
        self.assertEqual(len(checker.errors), 0)
        self.assertEqual(len(checker.warnings), 0)
        print(checker.errors)
        print(checker.warnings)

    def test_incorrect_parameter_types(self):
        checker = self.run_checker('test_incorrect_parameter_types.ska')
        self.assertGreater(len(checker.errors), 0)
        print(checker.errors)
        print(checker.warnings)

    def test_invalid_svg_reference(self):
        checker = self.run_checker('test_invalid_svg_reference.ska')
        self.assertGreater(len(checker.errors), 0)
        print(checker.errors)
        print(checker.warnings)

    def test_nonexistent_function_call(self):
        checker = self.run_checker('test_nonexistent_function_call.ska')
        self.assertGreater(len(checker.errors), 0)
        print(checker.errors)
        print(checker.warnings)

    def test_undefined_group_reference(self):
        checker = self.run_checker('test_undefined_group_reference.ska')
        self.assertGreater(len(checker.errors), 0)
        print(checker.errors)
        print(checker.warnings)

    def test_unused_parameters(self):
        checker = self.run_checker('test_unused_parameters.ska')
        self.assertGreater(len(checker.warnings), 0)
        print(checker.errors)
        print(checker.warnings)

if __name__ == '__main__':
    unittest.main()
