from antlr4.error.ErrorListener import ErrorListener

class ErrorListenerTest(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"Error at line {line}, column {column}: {msg}")

