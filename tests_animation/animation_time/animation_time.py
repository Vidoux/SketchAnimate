import xml.etree.ElementTree as ET
import cairosvg
import imageio.v2 as imageio
import os
import numpy as np

COLORS = ["red", "green", "blue", "yellow", "purple", "orange", "cyan"]


def modify_svg_color(input_svg, output_svg, color):
    """
    Modifie la couleur du trait (stroke) d'un carré SVG et l'enregistre.
    """
    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Cherche l'élément du rectangle
    rect_element = root.find(".//{http://www.w3.org/2000/svg}rect")
    if rect_element is not None:
        # Extraire les styles actuels
        style = rect_element.get("style")
        style_attributes = style.split(';')

        # Remplacer la couleur de trait
        new_style_attributes = []
        for attr in style_attributes:
            if attr.startswith("stroke:"):
                new_style_attributes.append(f"stroke:{color}")
            else:
                new_style_attributes.append(attr)

        # Mettre à jour les styles avec la nouvelle couleur
        rect_element.set("style", ";".join(new_style_attributes))
        tree.write(output_svg)

def main():
    input_svg = "square_input.svg"
    output_gif = "color.gif"

    images = []
    for color in COLORS:
        temp_svg = f"temp_{color}.svg"
        modify_svg_color(input_svg, temp_svg, color)
        output_png = f"temp_{color}.png"

        # Convertir SVG en PNG
        cairosvg.svg2png(url=temp_svg, write_to=output_png)

        # Lire l'image PNG et ajouter un fond blanc si nécessaire
        png_image = imageio.imread(output_png)
        if png_image.shape[2] == 4:  # Vérifier la présence d'un canal alpha
            # Convertir le canal alpha en un fond blanc
            white_background = np.ones_like(png_image[:, :, :3]) * 255
            alpha = png_image[:, :, 3:4] / 255.0
            png_image = (png_image[:, :, :3] * alpha + white_background * (1 - alpha)).astype(np.uint8)

        # Ajouter l'image deux fois pour augmenter la durée
        images.extend([png_image, png_image])

    # Créer un GIF à partir des images PNG
    imageio.mimsave(output_gif, images, duration=3)  # 3 seconde par image

    # Supprimer les fichiers PNG et SSVG intermédiaires
    for color in COLORS:
        os.remove(f"temp_{color}.png")
        os.remove(f"temp_{color}.svg")


if __name__ == "__main__":
    main()