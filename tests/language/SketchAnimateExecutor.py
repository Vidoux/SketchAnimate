from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmParser import SketchAnimateImperativeParadigmParser
from src.language.codegen.antlr_build.SketchAnimateImperativeParadigmVisitor import SketchAnimateImperativeParadigmVisitor
from tests.language.AnimationLib import SVGAnimationLib
import os
import shutil
from cairosvg import svg2png
import imageio
import numpy as np
from PIL import Image

class SketchAnimateExecutor(SketchAnimateImperativeParadigmVisitor):

    def __init__(self):
        # Initialiser un dictionnaire pour stocker les groupes
        self.groups = {}
        self.svg_path = ""
        self.actions = []
        self.duration_max = 0  # Durée maximale nécessaire

    def visitMainBlock(self, ctx: SketchAnimateImperativeParadigmParser.MainBlockContext):
        for statement in ctx.statement():
            self.visit(statement)

    def visitLoadSVGStatement(self, ctx: SketchAnimateImperativeParadigmParser.LoadSVGStatementContext):
        self.svg_path = ctx.STRING().getText() if ctx.STRING() else None

    def visitGroupDeclaration(self, ctx: SketchAnimateImperativeParadigmParser.GroupDeclarationContext):
        group_id = ctx.ID().getText()  # Nom du groupe
        members = [id.getText() for id in ctx.idList().ID()]  # Membres du groupe
        self.groups[group_id] = members
        print(f"Creating group {group_id} with members {members}")

    def visitAnimationStatement(self, ctx: SketchAnimateImperativeParadigmParser.AnimationStatementContext):
        if ctx.moveToStatement():
            self.visitMoveToStatement(ctx.moveToStatement())
        elif ctx.rotateStatement():
            self.visitRotateStatement(ctx.rotateStatement())
        elif ctx.changeColorStatement():
            self.visitChangeColorStatement(ctx.changeColorStatement())
        elif ctx.setVisibleStatement():
            self.visitSetVisibleStatement(ctx.setVisibleStatement())
        else:
            print("Unknown animation statement")

    def visitMoveToStatement(self, ctx: SketchAnimateImperativeParadigmParser.MoveToStatementContext):
        target, start_time, duration = ctx.target().getText(), int(ctx.startTime().getText()), int(ctx.duration().getText())
        # Retrieve x and y coordinates from moveToParams context
        move_to_params_ctx = ctx.moveToParams()
        x_coordinate, y_coordinate = float(move_to_params_ctx.expression(0).getText()), float(move_to_params_ctx.expression(1).getText())
        step_x = x_coordinate/(duration-start_time)
        step_y = y_coordinate/(duration-start_time)
        end_time = start_time + duration

        self.actions.append({
            'type': 'move',
            'target': target,
            'start_time': int(start_time),
            'end_time': end_time,
            'target_position': (x_coordinate, y_coordinate),
            'step': (step_x, step_y)
        })

    def visitRotateStatement(self, ctx: SketchAnimateImperativeParadigmParser.RotateStatementContext):
        target, start_time, duration = ctx.target().getText(), int(ctx.startTime().getText()), int(ctx.duration().getText())
        rotate_params_ctx = ctx.rotateParams()
        rotation_angle = int(rotate_params_ctx.expression().getText())
        end_time = start_time + duration
        step = rotation_angle/(duration-start_time)
        self.actions.append({
            'type': 'rotate',
            'target': target,
            'start_time': start_time,
            'end_time': end_time,
            'target_degree': rotation_angle,
            'step': step

        })

    def visitChangeColorStatement(self, ctx: SketchAnimateImperativeParadigmParser.ChangeColorStatementContext):
        target, start_time, duration = ctx.target().getText(), int(ctx.startTime().getText()), int(ctx.duration().getText())
        # Retrieve the new color from colorParams context
        color_params_ctx = ctx.colorParams()
        new_color = color_params_ctx.expression().getText()
        end_time = start_time + duration

        self.actions.append({
            'type': 'change_color',
            'target': target,
            'start_time': start_time,
            'end_time': end_time,
            'target_color': new_color,
        })

    def execute_actions(self):
        self.duration_max = 30
        self.svg_path = self.svg_path.replace('"', "")

        copy = "copy.svg"
        shutil.copyfile(self.svg_path, copy)

        svg_animation = SVGAnimationLib(copy)
        png_files = []

        for i in range(self.duration_max):
            for action in self.actions:
                if action['start_time'] <= i <= action['end_time']:
                    svg_animation.execute_action(action)

            # Export modified SVG to PNG
            png_filename = f"frame_{i:03}.png"
            svg_code = open("copy.svg", 'rt').read()
            svg2png(bytestring=svg_code, write_to=png_filename)
            png_files.append(png_filename)
        duration = 0.1
        # Create an animated GIF from the PNG files
        self.create_gif('output.gif', duration, png_files)

        # Clean up: Delete PNG files
        for file in png_files:
            os.remove(file)

    def add_background_to_png(self, png_path, bg_color=(255, 255, 255)):
        """Ajoute un fond opaque à une image PNG."""
        with Image.open(png_path) as img:
            with Image.new('RGB', img.size, bg_color) as background:
                background.paste(img, mask=img.split()[3])  # Utiliser le canal alpha comme masque
                background.save(png_path)

    def create_gif(self, output_gif_path, duration, png_files):
        """Crée un GIF à partir des images PNG stockées."""
        list_img = []

        for image_path in png_files:
            # Ajouter un fond à chaque image PNG
            self.add_background_to_png(image_path)
            png_image = imageio.imread(image_path)
            list_img.append(png_image)

        imageio.mimsave(output_gif_path, list_img, duration=duration, loop=0)
