import xml.etree.ElementTree as ET
import cairosvg
import imageio.v2 as imageio  # Utilisation de la version 2 pour éviter les avertissements de dépréciation
import os
import numpy as np

def modify_svg_scale(input_svg, output_svg, scale_factor):
    """
    Modifie l'échelle d'un rectangle SVG et l'enregistre.
    """
    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Cherche l'élément du rectangle
    rect_element = root.find(".//{http://www.w3.org/2000/svg}rect")
    if rect_element is not None:
        # Mise à jour des attributs de transformation pour l'échelle
        transform_str = f"scale({scale_factor})"
        rect_element.set("transform", transform_str)
        tree.write(output_svg)

def main():
    input_svg = "square_input.svg"
    output_gif = "scaling.gif"

    images = []

    # Échelle de 0.5 à 2.0 par incréments de 0.1 pour montrer l'agrandissement et la réduction
    for scale in np.arange(0.5, 2.1, 0.1):
        temp_svg = f"temp_{scale:.1f}.svg"
        modify_svg_scale(input_svg, temp_svg, scale)
        output_png = f"temp_{scale:.1f}.png"

        # Convertir SVG en PNG
        cairosvg.svg2png(url=temp_svg, write_to=output_png)

        # Lire l'image PNG et ajouter un fond blanc si nécessaire
        png_image = imageio.imread(output_png)
        if png_image.shape[2] == 4:  # Vérifier la présence d'un canal alpha
            # Convertir le canal alpha en un fond blanc
            white_background = np.ones_like(png_image[:, :, :3]) * 255
            alpha = png_image[:, :, 3:4] / 255.0
            png_image = (png_image[:, :, :3] * alpha + white_background * (1 - alpha)).astype(np.uint8)
        images.append(png_image)

    # Créer un GIF à partir des images PNG
    imageio.mimsave(output_gif, images, duration=0.1)  # 0.1 seconde par image

    # Supprimer les fichiers PNG et SVG intermédiaires
    for scale in np.arange(0.5, 2.1, 0.1):
        os.remove(f"temp_{scale:.1f}.png")
        os.remove(f"temp_{scale:.1f}.svg")

if __name__ == "__main__":
    main()
