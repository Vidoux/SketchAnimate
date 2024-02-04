from xml.etree import ElementTree as ET
import re
import cairosvg
import imageio.v2 as imageio
import os
import numpy as np
from PIL import Image

images = []

class SVGAnimationLib:
    def __init__(self, svg_content):
        copy_file_path = 'square_input_copy.svg'
        with open(copy_file_path, 'r') as file:
            svg_content = file.read()

        self.tree = ET.ElementTree(ET.fromstring(svg_content))
        self.namespace = {'svg': 'http://www.w3.org/2000/svg'}
        self.rect = self.tree.find('.//svg:rect', self.namespace)
        self.temp_files = []

    def moveTarget(self, target_position, steps=10):
        # Convertir les valeurs de position en float
        x1, y1 = map(float, target_position)

        # TODO verifier les types des params
        x0, y0 = self.get_current_position()
        for step in range(1, steps + 1):
            intermediate_x = x0 + (x1 - x0) * step / steps
            intermediate_y = y0 + (y1 - y0) * step / steps
            self.rect.set('x', str(intermediate_x))
            self.rect.set('y', str(intermediate_y))
            self.save_state_as_png(f"move_{intermediate_x}_{intermediate_y}")

    def rotateTarget(self, target_degree, clockwise=True, steps=40):
        initial_degree = self.get_current_rotation()

        if clockwise:
            # Rotation dans le sens des aiguilles d'une montre
            degree_increment = (int(target_degree[0]) - initial_degree) / steps
        else:
            # Rotation dans le sens inverse des aiguilles d'une montre
            degree_increment = (initial_degree - int(target_degree[0])) / steps

        for step in range(1, steps + 1):
            new_degree = initial_degree + degree_increment * step
            self.apply_rotation(new_degree)
            self.save_state_as_png(f"rotate_{new_degree}")

    def resizeTarget(self, target_size, steps=10):
        initial_width, initial_height = self.get_current_size()
        initial_x, initial_y = self.get_current_position()

        target_width, target_height = map(float, target_size)

        for step in range(1, steps + 1):
            new_width = initial_width + (target_width - initial_width) * step / steps
            new_height = initial_height + (target_height - initial_height) * step / steps

            # Calculer les décalages pour maintenir le centre
            delta_width = new_width - initial_width
            delta_height = new_height - initial_height
            new_x = initial_x - delta_width / 2
            new_y = initial_y - delta_height / 2

            self.rect.set('width', str(new_width))
            self.rect.set('height', str(new_height))
            self.rect.set('x', str(new_x))
            self.rect.set('y', str(new_y))
            self.save_state_as_png(f"resize_{new_width}_{new_height}")
        self.save_svg("square_input_copy.svg")

    def changeColorTarget(self, target_color):
        self.apply_color(target_color)
        self.save_svg("square_input_copy.svg")

    def apply_color(self, color):
        # Appliquer la nouvelle couleur
        style = self.rect.get('style', '')
        new_style = re.sub(r'fill:[^;]+;', f'fill:{color[0]};', style)
        if 'fill:' not in style:
            new_style = f"{style} fill:{color};"
        self.rect.set('style', new_style)


    def save_svg(self, filename):
        """Sauvegarde l'état actuel du SVG dans un fichier."""
        svg_content = ET.tostring(self.tree.getroot(), encoding='unicode')
        with open(filename, 'w') as file:
            file.write(svg_content)

    def get_current_position(self):
        x = float(self.rect.get('x', '0'))
        y = float(self.rect.get('y', '0'))
        return x, y

    def get_current_rotation(self):
        # Simplification: suppose que la rotation est le seul élément de transformation
        transform = self.rect.get('transform', '')
        match = re.search(r'rotate\(([\d.-]+)\)', transform)
        return float(match.group(1)) if match else 0

    def apply_rotation(self, degree):
        self.rect.set('transform', f'rotate({degree})')

    def get_current_size(self):
        width = float(self.rect.get('width', '0'))
        height = float(self.rect.get('height', '0'))
        return width, height

    def save_state_as_png(self, filename):
        """Sauvegarder l'état actuel en tant que PNG avec un fond opaque."""
        temp_svg = filename + '.svg'
        temp_png = filename + '.png'
        svg_content = ET.tostring(self.tree.getroot(), encoding='unicode')
        with open(temp_svg, 'w') as file:
            file.write(svg_content)

        # Convertir le fichier SVG en PNG
        cairosvg.svg2png(url=temp_svg, write_to=temp_png)

        # Ajouter un fond opaque à l'image PNG
        with Image.open(temp_png) as img:
            # Créer une nouvelle image avec un fond blanc
            with Image.new("RGB", img.size, "WHITE") as background:
                # Coller l'image PNG sur le fond blanc
                background.paste(img, mask=img.split()[3])  # 3 est l'indice du canal alpha dans le mode "RGBA"
                background.save(temp_png, "PNG")

        # Ajouter le fichier PNG à la liste des images
        images.append(temp_png)
        self.temp_files.append(temp_png)

        # Supprimer le fichier SVG temporaire
        os.remove(temp_svg)

    def get_svg_content(self):
        """Récupérer le contenu SVG actuel."""
        return ET.tostring(self.tree.getroot(), encoding='unicode')

    def create_gif(self, output_gif_path, duration=0.1):
        """Crée un GIF à partir des images PNG stockées."""
        # Créer un GIF à partir des images PNG
        list_img = []
        # Lire l'image PNG et ajouter un fond blanc si nécessaire
        for image_path in images:
            png_image = imageio.imread(image_path)
            if png_image.shape[2] == 4:
                # Conversion du canal alpha en fond blanc
                white_background = np.ones_like(png_image[:, :, :3]) * 255
                alpha_layer = png_image[:, :, 3] / 255.0
                for channel in range(3):
                    png_image[:, :, channel] = png_image[:, :, channel] * alpha_layer + white_background[:, :,
                                                                                        channel] * (1 - alpha_layer)
            list_img.append(png_image)

        # Création du gif
        imageio.mimsave(output_gif_path, list_img, duration=duration, loop=0)

        self.cleanup()

    def cleanup(self):
        """Supprime les fichiers PNG temporaires."""
        global images
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        images = []
        self.temp_files = []
