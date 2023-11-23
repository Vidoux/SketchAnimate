from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import SketchAnimateImperativeParadigmVisitor


class SketchAnimateExecutor(SketchAnimateImperativeParadigmVisitor):

    def visitAnimationStatement(self, ctx: SketchAnimateImperativeParadigmParser.AnimationStatementContext):
        print("visiting AnimationStatement")

