from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import SketchAnimateImperativeParadigmVisitor


class SketchAnimateExecutor(SketchAnimateImperativeParadigmVisitor):

    def __init__(self):
        # Initialiser un dictionnaire pour stocker les groupes
        self.groups = {}

    def visitGroupDeclaration(self, ctx: SketchAnimateImperativeParadigmParser.GroupDeclarationContext):
        group_id = ctx.ID().getText()  # Nom du groupe
        members = [id.getText() for id in ctx.idList().ID()]  # Membres du groupe
        self.groups[group_id] = members
        print(f"Creating group {group_id} with members {members}")

    def visitAnimationStatement(self, ctx: SketchAnimateImperativeParadigmParser.AnimationStatementContext):
        target_id = ctx.target().getText()  # Cible de l'animation
        action = ctx.action().getText()  # Type d'action
        print(f"Animating {target_id} with action {action}")

        # Ici, vous pouvez ajouter la logique pour exécuter l'action sur la cible
