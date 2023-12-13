from antlr4.error.ErrorListener import ErrorListener


class SketchAnimateErrorListener(ErrorListener):
    def __init__(self):
        super(SketchAnimateErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Line {line}:{column} - {msg}"
        self.errors.append(error_message)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        if not exact:
            message = f"Ambiguity detected: From {startIndex} to {stopIndex}"
            self.errors.append(message)
