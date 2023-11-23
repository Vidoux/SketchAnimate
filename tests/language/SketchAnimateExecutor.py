from src.language.codegen.antlr_build.SketchAnimateParser import SketchAnimateParser
from src.language.codegen.antlr_build.SketchAnimateVisitor import SketchAnimateVisitor


class SketchAnimateExecutor(SketchAnimateVisitor):

    def visitObjectDeclaration(self, ctx: SketchAnimateParser.ObjectDeclarationContext):
        print("visiting ObjectDeclaration" + ctx.ID().getText())

    def visitAnimationStatement(self, ctx: SketchAnimateParser.AnimationStatementContext):
        print("visiting AnimationStatement" + ctx.ID().getText())

