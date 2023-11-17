import os
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget
from xml.etree import ElementTree

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddIdsToSVG(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.svgWidget = QSvgWidget()
        self.layout.addWidget(self.svgWidget)

        self.setWindowTitle('Add IDs to SVG')
        self.setGeometry(100, 100, 800, 600)
        self.show()

        self.loadAndAddIds()

    def loadAndAddIds(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "SVG files (*.svg)")
        if fname:
            logger.info(f"Loading and processing SVG: {fname}")
            svg_data = self.addIdsToSvg(fname)
            if svg_data is not None:
                new_fname = self.addStringToFileName(fname, '_with_id')
                self.saveSvg(new_fname, svg_data)
                logger.info(f"SVG with added IDs saved as: {new_fname}")

    @staticmethod
    def addIdsToSvg(fname):
        try:
            tree = ElementTree.parse(fname)
            root = tree.getroot()
            element_counter = {}
            for elem in root.iter():
                if 'id' not in elem.attrib:
                    tag = elem.tag.split('}')[-1]
                    if tag in element_counter:
                        element_counter[tag] += 1
                    else:
                        element_counter[tag] = 1
                    elem.attrib['id'] = f'{tag}{element_counter[tag]}'
            return ElementTree.tostring(root, encoding='unicode')
        except Exception as e:
            logger.error(f"Error parsing SVG: {e}")
            return None

    def addStringToFileName(self, fname, suffix):
        base, ext = os.path.splitext(fname)
        new_fname = f'{base}{suffix}{ext}'
        return new_fname

    def saveSvg(self, fname, svg_data):
        if svg_data is not None:
            with open(fname, 'w', encoding='utf-8') as svg_file:
                svg_file.write(svg_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddIdsToSVG()
    sys.exit(app.exec_())
