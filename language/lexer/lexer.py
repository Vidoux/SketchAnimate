# -*- encoding: utf-8 -*-

import re
from constants import LEXEM_REGEXES

import logging

logger = logging.getLogger(__name__)


class LexerException(Exception):
    pass


class Lexem:
    """
    Our lexem (token) definition with the attributes:
    - Tag: Type of the lexem, matched with the regex
    - Value: Its actual value (e.g. the identifier name)
    - Position: Line number and position in the line
    """

    def __init__(self, tag, value, position):
        self.tag = tag
        self.value = value
        self.position = position

    def __repr__(self):
        return f"{self.tag}({self.value})"


class Lexer:
    def __init__(self):
        """
        Component in charge lexical analysis.
        """
        self.lexems = []
        self.current_line_number = 0
        self.current_position = 0

    # ==========================
    #     Matching Functions
    # ==========================

    def lex_file(self, file):
        """
        Opens a file and runs the lexer through its contents.
        """
        with open(file, "r") as input_file:
            contents = input_file.readlines()
        return self.lex(contents)

    def lex(self, input):
        """
        Creates a lexem for every matched regular expression.
        Crawls through the input (list of lines).
        """
        for line_nb, line in enumerate(input):
            self.current_position = 0
            self.current_line_number = (
                line_nb + 1
            )  # Python starts at 0, we need to start at 1
            line = line.strip()
            try:
                self.match_line(line)
            except LexerException as err:
                logger.exception(err)
                raise
        return self.lexems

    def match_line(self, line):
        """
        Tries to match a line with all regexes.
        """
        while self.current_position < len(line):
            # Test all regexes in order
            match = False
            for lexem_regex in LEXEM_REGEXES:
                match = self.match_lexem(line, lexem_regex)
                # If a match occurs, break from the loop
                if match:
                    break
            # If all regexes were tested and none matched,
            # raise an error!
            if not match:
                raise LexerException(
                    f"ERROR (lexer) at: ({self.current_line_number},{self.current_position}):\n"
                    + line.strip() + "\n"
                    + " " * len(line[: self.current_position])
                    + "^" * len(line[self.current_position - 1 :])
                    + f"\nLexems: {self.lexems}"
                )

    def match_lexem(self, line, lexem_regex):
        """
        Matches the line with a given regex/tag.
        """
        pattern, tag = lexem_regex
        # Compile and match the regex
        #print(pattern)
        regex = re.compile(pattern)
        match = regex.match(line, self.current_position)
        # If a match occured, the result is not None
        if match is not None:
            data = match.group(0)
            # If the match was with a whitespace, its tag is None
            # and we do not need to keep it
            if tag is not None:
                self.append_lexem(tag, data)
            self.current_position = match.end(0)
            return True
        return False

    def append_lexem(self, tag, data):
        """
        Creates and adds a new lexem to the list
        """
        lexem = Lexem(tag, data, [self.current_line_number, self.current_position])
        self.lexems.append(lexem)
