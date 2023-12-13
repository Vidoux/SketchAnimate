from xml.etree import ElementTree as ET
import re
import cairosvg
import imageio.v2 as imageio
import os
import numpy as np

class SVGAnimationLib:
    def __init__(self, svg_content):
        self.tree = ET.ElementTree(ET.fromstring(svg_content))
        self.namespace = {'svg': 'http://www.w3.org/2000/svg'}
        self.rect = self.tree.find('.//svg:rect', self.namespace)

    def moveTarget(self, position):
        x, y = position
        self.rect.set('x', str(x))
        self.rect.set('y', str(y))

    def rotateTarget(self, degree):
        current_transform = self.rect.get('transform', '')
        new_transform = f"rotate({degree})"
        self.rect.set('transform', new_transform if not current_transform else f"{current_transform} {new_transform}")

    def resizeTarget(self, new_size):
        width, height = new_size
        self.rect.set('width', str(width))
        self.rect.set('height', str(height))

    def changeColorTarget(self, color):
        style = self.rect.get('style', '')
        color_style = f"fill:{color};"
        new_style = re.sub(r'fill:[^;]+;', color_style, style)
        if 'fill:' not in style:
            new_style = f"{style} {color_style}"
        self.rect.set('style', new_style)

    def get_svg_content(self):
        return ET.tostring(self.tree.getroot(), encoding='unicode')


"""
# Assurez-vous d'inclure le chemin correct vers votre fichier SVG
file_path = 'square_input.svg'

# Lire le contenu du fichier SVG
with open(file_path, 'r') as file:
    svg_content = file.read()

# Créer une instance de SVGAnimationLib avec le contenu SVG
svg_lib = SVGAnimationLib(svg_content)


# Appliquer les actions
svg_lib.moveTarget((200, 200))
svg_lib.rotateTarget(45)
svg_lib.resizeTarget((150, 150))
svg_lib.changeColorTarget("red")

"""