from antlr4 import *
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import \
    SketchAnimateImperativeParadigmVisitor
import xml.etree.ElementTree as ElementTree

###
# TODO:
# - Ajout vérification paramètres non-utilisés dans les fonctions
# -
###



class SketchAnimateChecker(SketchAnimateImperativeParadigmVisitor):
    def __init__(self):
        self.symbolTable = {}
        self.errors = []

    def visitMainBlock(self, ctx: SketchAnimateImperativeParadigmParser.MainBlockContext):
        for statement in ctx.statement():
            self.visit(statement)

    # TODO Externaliser la fonction car aussi utile dans Executor
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
        except Exception as e:
            raise SVGFileLoadError(svg_path, str(e))

    def visitLoadSVGStatement(self, ctx: SketchAnimateImperativeParadigmParser.LoadSVGStatementContext):
        svg_path = ctx.STRING().getText().strip('"')
        try:
            svg_elements = SketchAnimateChecker.loadSVGElements(svg_path)
            for element in svg_elements:
                self.symbolTable[element] = {'type': 'svg_element'}
        except SVGFileLoadError as e:
            line = ctx.start.line
            column = ctx.start.column
            self.errors.append(e)

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

        # Supprimer les paramètres de la séquence de la table des symboles après l'analyse
        if ctx.parameterList():
            for param in ctx.parameterList().parameter():
                param_name = param.getText()
                del self.symbolTable[param_name]

    def visitAnimationStatement(self, ctx: SketchAnimateImperativeParadigmParser.AnimationStatementContext):
        target = ctx.target().getText()
        line = ctx.start.line
        column = ctx.start.column
        if target not in self.symbolTable:
            self.errors.append(UndefinedSymbolError(target, line, column))
            return

    def reportErrors(self):
        print(self.symbolTable)
        if self.errors:
            for error in self.errors:
                print(str(error))
            raise Exception("Analysis completed with multiple errors.")


# ---- Redefine Error handling ----
# TODO externaliser dans un autre fichier
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
        message = f"Erreur lors du chargement du fichier SVG '{svg_path}': {error_message}"
        super().__init__(message)
