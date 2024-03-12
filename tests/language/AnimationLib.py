from lxml import etree
import re

class SVGAnimationLib:
    def __init__(self, svg_path):
        self.svg_path = svg_path
        with open(svg_path, 'r') as file:
            svg_content = file.read()

        self.tree = etree.fromstring(svg_content.encode())

    def save_changes(self):
        # Enregistrer les modifications dans le fichier SVG
        with open(self.svg_path, 'wb') as file:
            file.write(etree.tostring(self.tree, pretty_print=True))

    def execute_action(self, action):
        action_type = action['type']
        target = action['target']

        # Utiliser XPath avec lxml
        self.element = self.tree.xpath(f"//*[@id='{target}']")

        if not self.element:
            print(f"Error: Target element '{target}' not found in SVG")
            return
        if action_type == 'move':
            self._execute_move_action(action)
        elif action_type == 'rotate':
            self._execute_rotate_action(action)
        elif action_type == 'change_color':
            self._execute_change_color_action(action)
        else:
            print(f"Warning: Unknown action type '{action_type}'")
        self.save_changes()

    def _execute_move_action(self, action):
        x_step, y_step = action['step']

        elem = self.element[0] if self.element else None

        if elem is not None:
            local_tag = etree.QName(elem).localname

            if local_tag == 'circle':
                cx = float(elem.get('cx', '0'))
                cy = float(elem.get('cy', '0'))
                elem.set('cx', str(cx + x_step))
                elem.set('cy', str(cy + y_step))

            elif local_tag == 'rect':
                x = float(elem.get('x', '0'))
                y = float(elem.get('y', '0'))
                elem.set('x', str(x + x_step))
                elem.set('y', str(y + y_step))

            elif local_tag == 'polygon':
                points = elem.get('points').split()
                new_points = []
                for point in points:
                    x, y = map(float, point.split(','))
                    new_points.append(f"{x + x_step},{y + y_step}")
                elem.set('points', ' '.join(new_points))

            elif local_tag == 'line':
                x1 = float(elem.get('x1', '0'))
                y1 = float(elem.get('y1', '0'))
                x2 = float(elem.get('x2', '0'))
                y2 = float(elem.get('y2', '0'))
                elem.set('x1', str(x1 + x_step))
                elem.set('y1', str(y1 + y_step))
                elem.set('x2', str(x2 + x_step))
                elem.set('y2', str(y2 + y_step))

            else:
                print(f"Error: Unsupported element type '{local_tag}' for move action.")
        else:
            print("Error: No element found.")

    def _get_center_of_element(self, elem):
        if etree.QName(elem).localname == 'circle':
            cx = float(elem.get('cx', '0'))
            cy = float(elem.get('cy', '0'))
            return cx, cy
        elif etree.QName(elem).localname == 'rect':
            x = float(elem.get('x', '0'))
            y = float(elem.get('y', '0'))
            width = float(elem.get('width', '0'))
            height = float(elem.get('height', '0'))
            return x + width / 2, y + height / 2
        # Ajouter ici le calcul du centre pour d'autres éléments si nécessaire
        return None, None  # Retourne None si le centre ne peut être calculé

    def _execute_rotate_action(self, action):
        step = action['step']

        elem = self.element[0] if self.element else None

        if elem is not None:
            cx, cy = self._get_center_of_element(elem)
            if cx is not None and cy is not None:
                # Construction de la valeur de l'attribut transform pour la rotation
                transform = elem.get('transform', '')
                new_transform = f"rotate({step} {cx} {cy}) " + transform
                elem.set('transform', new_transform)
            else:
                print(f"Error: Unable to determine center for rotation.")
        else:
            print("Error: No element found.")

    def _execute_change_color_action(self, action):
        new_color = action['target_color'].strip('"')  # Retire les guillemets si présents

        elem = self.element[0] if self.element else None

        if elem is not None:
            # Construire ou mettre à jour l'attribut 'style'
            style = elem.get('style', '')
            if 'fill' in style:
                style = re.sub(r'(?<=fill:)[^;]+', new_color, style)
            else:
                style += f";fill:{new_color}"

            if 'stroke' in style:
                style = re.sub(r'(?<=stroke:)[^;]+', new_color, style)
            else:
                style += f";stroke:{new_color}"

            elem.set('style', style.strip(';'))
        else:
            print("Error: No element found.")


svg_animator = SVGAnimationLib('./lexer_parser/example.svg')
svg_animator.execute_action({'type': 'change_color', 'target': 'circle1', 'target_color': "red"})
