import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QMimeData
from xml.etree import ElementTree


class SVGViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.svg_data = None
        self.svgWidget = None
        self.layout = None
        self.centralWidget = None
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.svgWidget = QSvgWidget()
        self.layout.addWidget(self.svgWidget)

        self.setWindowTitle('SVG Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.show()

        self.loadSvg()

    def loadSvg(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "SVG files (*.svg)")
        if fname:
            self.svgWidget.load(fname)
            self.svg_data = self.extractSvgData(fname)

    def extractSvgData(self, fname):
        svg_data = {}
        try:
            tree = ElementTree.parse(fname)
            root = tree.getroot()
            for elem in root.iter():
                if 'id' in elem.attrib:
                    svg_data[elem.attrib['id']] = elem
        except Exception as e:
            print(f"Error parsing SVG: {e}")
        return svg_data

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Get the position of the mouse click in global coordinates
            global_pos = event.globalPos()
            # Map the global coordinates to coordinates in the QMainWindow
            local_pos = self.mapFromGlobal(global_pos)
            # Map the local coordinates to coordinates in the QSvgWidget
            svg_pos = self.svgWidget.mapFromParent(local_pos)
            for elem_id, elem in self.svg_data.items():
                if elem.get('x') and elem.get('y'):
                    x = float(elem.get('x'))
                    y = float(elem.get('y'))
                    width = float(elem.get('width'))
                    height = float(elem.get('height'))
                    if x <= svg_pos.x() <= x + width and y <= svg_pos.y() <= y + height:
                        # Display the ID in a message box
                        QMessageBox.information(self, 'Element ID', f'Clicked on element with ID: {elem_id}')
                        # Copy the ID to the clipboard
                        clipboard = QApplication.clipboard()
                        mime_data = QMimeData()
                        mime_data.setText(elem_id)
                        clipboard.setMimeData(mime_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SVGViewer()
    sys.exit(app.exec_())