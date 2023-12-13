from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import SketchAnimateImperativeParadigmVisitor
from src.animation.AnimationLib import SVGAnimationLib
import os
from PIL import Image

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
        # Récupérer les paramètres de l'action
        parameters_ctx = ctx.actionParameters()
        parameters = [param.getText() for param in parameters_ctx.parameter()]

        if target_id in self.groups:
            for member in self.groups[target_id]:
                self.executeAction(member, action, parameters)
        else:
            self.executeAction(target_id, action, parameters)

        print(f"Animating {target_id} with action {action}")

    def executeAction(self,target, action, parameters):
        file_path = 'square_input.svg'

        # Lire le contenu du fichier SVG
        with open(file_path, 'r') as file:
            svg_content = file.read()

        anim_lib = SVGAnimationLib(svg_content)

        if action == "moveTo":
            anim_lib.moveTarget(parameters)

        elif action == "rotate":
            anim_lib.rotateTarget(parameters)

        elif action == "resize":
            anim_lib.resizeTarget(parameters)

        elif action == "changeColor":
            anim_lib.changeColorTarget(parameters)
        else:
            print(f"Unknown action: {action}")

        updated_svg_content = anim_lib.get_svg_content()

        with open('updated_square.svg', 'w') as file:
            file.write(updated_svg_content)
