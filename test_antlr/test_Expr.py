__author__ = 'jszheng'

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from antlr_build.ExprLexer import ExprLexer
from antlr_build.ExprParser import ExprParser

if __name__ == '__main__':
    input_stream = FileStream("t.expr")

    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.prog()

    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)
