import xml.etree.ElementTree as ET
import cairosvg
import imageio.v2 as imageio  # Utilisation de la version 2 pour éviter les avertissements de dépréciation
import math


def modify_svg_rotation(input_svg, output_svg, rotation_degree):
    """
    Modifie la rotation d'un carré SVG autour de son coin inférieur droit et l'enregistre.
    """
    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Cherche l'élément du rectangle
    rect_element = root.find(".//{http://www.w3.org/2000/svg}rect")
    if rect_element is not None:
        # Calcul de la translation en X en fonction de la rotation pour simuler le roulement
        translation = 300 * (1 - math.cos(math.radians(rotation_degree)))

        # Mise à jour des attributs de transformation pour rotation et translation
        transform_str = f"rotate({rotation_degree} 400 400) translate({translation} 0)"
        rect_element.set("transform", transform_str)
        tree.write(output_svg)


def main():
    input_svg = "square_input.svg"  # Sauvegardez votre SVG avec ce nom ou modifiez cette ligne
    output_gif = "rolling_rectangle.gif"

    images = []

    for degree in range(0, 361, 10):  # Rotation de 0 à 360 degrés par incréments de 10 degrés
        temp_svg = f"temp_{degree}.svg"
        modify_svg_rotation(input_svg, temp_svg, degree)
        output_png = f"temp_{degree}.png"

        # Convertir SVG en PNG
        cairosvg.svg2png(url=temp_svg, write_to=output_png)

        images.append(imageio.imread(output_png))

    # Créer un GIF à partir des images PNG
    imageio.mimsave(output_gif, images, duration=0.1)  # 0.1 seconde par image


if __name__ == "__main__":
    main()
