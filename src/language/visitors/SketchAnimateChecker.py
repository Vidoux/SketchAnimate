import re


from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import \
    SketchAnimateImperativeParadigmVisitor
import xml.etree.ElementTree as ElementTree
import warnings


class SketchAnimateChecker(SketchAnimateImperativeParadigmVisitor):
    def __init__(self):
        self.symbolTable = {}
        self.errors = []
        self.warnings = []

    def visitMainBlock(self, ctx: SketchAnimateImperativeParadigmParser.MainBlockContext):
        for statement in ctx.statement():
            self.visit(statement)

    @staticmethod
    def loadSVGElements(svg_path):
        try:
            tree = ElementTree.parse(svg_path)
            root = tree.getroot()
            svg_element_ids = []
            for element in root.iter():
                if 'id' in element.attrib:
                    svg_element_ids.append(element.attrib['id'])
            return svg_element_ids
        except FileNotFoundError as e:
            raise SVGFileLoadError(svg_path, str(e))

    def visitLoadSVGStatement(self, ctx: SketchAnimateImperativeParadigmParser.LoadSVGStatementContext):
        svg_path = ctx.STRING().getText().strip('"')
        try:
            svg_elements = SketchAnimateChecker.loadSVGElements(svg_path)
            for element in svg_elements:
                self.symbolTable[element] = {'type': 'svg_element'}
        except SVGFileLoadError as e:
            self.errors.append(e)
            return  # Arrêtez le traitement ultérieur si c'est une erreur critique

    def visitGroupDeclaration(self, ctx: SketchAnimateImperativeParadigmParser.GroupDeclarationContext):
        group_name = ctx.ID().getText()
        line = ctx.start.line
        column = ctx.start.column
        elements = [element.getText() for element in ctx.idList().ID()]

        if group_name in self.symbolTable:
            self.errors.append(RedefinitionError(group_name, line, column))
        else:
            self.symbolTable[group_name] = {'type': 'group', 'elements': []}

        for element_name in elements:
            if element_name not in self.symbolTable or self.symbolTable[element_name]['type'] != 'svg_element':
                # Si l'élément n'est pas défini en tant qu'élément SVG, ajouter une erreur
                self.errors.append(UndefinedSymbolError(element_name, line, column))
            else:
                # Si l'élément est défini, l'ajouter au groupe
                self.symbolTable[group_name]['elements'].append(element_name)

    def visitSequence(self, ctx: SketchAnimateImperativeParadigmParser.SequenceContext):
        sequence_name = ctx.ID().getText()
        line = ctx.start.line
        column = ctx.start.column
        if sequence_name in self.symbolTable:
            self.errors.append(RedefinitionError(sequence_name, line, column))
            return
        self.symbolTable[sequence_name] = {'type': 'sequence'}

        # Enregistrer les paramètres de la séquence
        if ctx.parameterList():
            for param in ctx.parameterList().parameter():
                param_name = param.getText()
                # Enregistrer le paramètre comme un identifiant temporaire valide dans la séquence
                self.symbolTable[param_name] = {'type': 'parameter'}

        # Visiter chaque instruction dans la séquence
        for statement in ctx.statement():
            self.visit(statement)

        # Check for unused parameters
        defined_parameters = self.symbolTable[sequence_name].get('parameters', set())
        for param in defined_parameters:
            if param not in self.symbolTable:
                self.warnings.append(UnusedParameterWarning(param, line, column))

        # Supprimer les paramètres de la séquence de la table des symboles après l'analyse
        if ctx.parameterList():
            for param in ctx.parameterList().parameter():
                param_name = param.getText()
                del self.symbolTable[param_name]

    def visitMoveToStatement(self, ctx: SketchAnimateImperativeParadigmParser.MoveToStatementContext):
        if self.checkTarget(ctx.target().getText(), ctx):
            self.visit(ctx.moveToParams())

    def visitRotateStatement(self, ctx: SketchAnimateImperativeParadigmParser.RotateStatementContext):
        if self.checkTarget(ctx.target().getText(), ctx):
            self.visit(ctx.rotateParams())

    def visitChangeColorStatement(self, ctx: SketchAnimateImperativeParadigmParser.ChangeColorStatementContext):
        if self.checkTarget(ctx.target().getText(), ctx):
            self.visit(ctx.colorParams())

    def visitSetVisibleStatement(self, ctx: SketchAnimateImperativeParadigmParser.SetVisibleStatementContext):
        if self.checkTarget(ctx.target().getText(), ctx):
            self.visit(ctx.visibilityParams())

    def visitResizeStatement(self, ctx: SketchAnimateImperativeParadigmParser.SetVisibleStatementContext):
        if self.checkTarget(ctx.target().getText(), ctx):
            self.visit(ctx.resizeParams())

    def checkTarget(self, target, ctx):
        if target not in self.symbolTable:
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(UndefinedSymbolError(target, line, column))
            return False
        return True

    def visitMoveToParams(self, ctx: SketchAnimateImperativeParadigmParser.MoveToParamsContext):
        x, y = ctx.expression()
        if not self.isNumber(x) or not self.isNumber(y):
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(TypeError("moveTo", "x, y", "number (float or int)", line, column))

    def visitRotateParams(self, ctx):
        if ctx is not None:
            angle = ctx.expression()
            if not self.isNumber(angle):
                line = ctx.start.line
                column = ctx.start.column
                self.errors.append(TypeError("rotate", "angle", "number", line, column))

    def visitChangeColorParams(self, ctx):
        colorValue = ctx.expression()
        if not self.isValidColor(colorValue):
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(TypeError("changeColor", "color", "valid color format", line, column))

    def visitSetVisibleParams(self, ctx):
        visibility = ctx.expression()
        if not visibility.getText() in ["true", "false"]:
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(TypeError("setVisible", "visibility", "boolean", line, column))

    def visitResizeParams(self, ctx: SketchAnimateImperativeParadigmParser.ResizeParamsContext):
        x, y = ctx.expression()
        if not self.isNumber(x) or not self.isNumber(y):
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(TypeError("resize", "x, y", "number (float or int)", line, column))

    def visitExportParams(self, ctx):
        path_param = ctx.pathParam().getText().strip('"')
        if not self.isPathValid(path_param):
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(TypeError("exportAnimation", "path", "valid file path", line, column))

    def visitSequenceInvocation(self, ctx: SketchAnimateImperativeParadigmParser.SequenceInvocationContext):
        sequence_name = ctx.ID().getText()
        line = ctx.start.line
        column = ctx.start.column

        if sequence_name not in self.symbolTable or self.symbolTable[sequence_name]['type'] != 'sequence':
            self.errors.append(UndefinedSymbolError(sequence_name, line, column))
            return

        sequence_definition = self.symbolTable[sequence_name]
        passed_parameters = ctx.argumentList().expression() if ctx.argumentList() else []

        defined_parameters = sequence_definition.get('parameters', [])
        if len(passed_parameters) != len(defined_parameters):
            self.errors.append(
                TypeError(sequence_name, f"Expected {len(defined_parameters)} parameters, got {len(passed_parameters)}",
                          line, column))
            return

    @staticmethod
    def isPathValid(path_param):
        # check if path is not blank (empty or only spaces)
        if not path_param or path_param.isspace():
            return False
        return True

    # Pattern: #FFFFFF ou #FFF
    @staticmethod
    def isValidColor(expression):
        hex_color_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        return hex_color_pattern.match(expression.getText().strip('"'))
        pass


    @staticmethod
    def isNumber(expression):
        if expression is None:
            return False

        if isinstance(expression, SketchAnimateImperativeParadigmParser.ExpressionContext):
            # Vérifier si l'expression contient un littéral
            literal = expression.literal()
            if literal is not None:
                # Vérifier si le littéral est un INT ou un FLOAT
                return literal.INT() is not None or literal.FLOAT() is not None
        return False

    def reportErrors(self):
        if self.errors:
            for error in self.errors:
                print(f"Error: {error}")
            raise Exception("Analysis completed with errors.")

        if self.warnings:
            for warning in self.warnings:
                warnings.warn(f"Warning: {warning}")


# ---- Redefine Error handling ----
class RedefinitionError(Exception):
    def __init__(self, symbol, line, column):
        message = f"Line {line}, Column {column}: Redefinition of '{symbol}'"
        super().__init__(message)


class UndefinedSymbolError(Exception):
    def __init__(self, symbol, line, column):
        message = f"Line {line}, Column {column}: Undefined symbol '{symbol}'"
        super().__init__(message)


class InvalidUsageError(Exception):
    def __init__(self, symbol, line, column):
        message = f"Line {line}, Column {column}: Invalid usage of '{symbol}'"
        super().__init__(message)


class MissingPositionalArgumentError(Exception):
    def __init__(self, argument_name, line, column):
        message = f"Line {line}, Column {column}: Missing required positional argument '{argument_name}'"
        super().__init__(message)


class SVGFileLoadError(Exception):
    def __init__(self, svg_path, error_message):
        self.message = f"Error loading SVG file '{svg_path}': {error_message}"
        super().__init__(self.message)


class UnusedParameterWarning(Warning):
    def __init__(self, param_name, line, column):
        self.message = f"Line {line}, Column {column}: Unused parameter '{param_name}'"
        super().__init__(self.message)


class TypeError(Exception):
    def __init__(self, action, parameter, expected_type, line, column):
        message = f"Line {line}, Column {column}: Invalid type for '{parameter}' in '{action}'. Expected {expected_type}."
        super().__init__(message)
