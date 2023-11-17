import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QFileDialog, QWidget, QVBoxLayout, \
    QMessageBox, QPushButton
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QCursor, QPixmap, QPainter
from xml.etree import ElementTree

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SVGViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.zoom_out_button = None

        self.svgWidget = None
        self.svg_data = None
        self.view = None
        self.scene = None
        self.renderer = None
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Create a QGraphicsView and QGraphicsScene to display the SVG
        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        # Create zoom buttons
        self.zoom_in_button = QPushButton('Zoom In', self)
        self.zoom_out_button = QPushButton('Zoom Out', self)

        self.layout.addWidget(self.zoom_in_button)
        self.layout.addWidget(self.zoom_out_button)

        # Connect zoom buttons to zoom functions
        self.zoom_in_button.clicked.connect(self.zoomIn)
        self.zoom_out_button.clicked.connect(self.zoomOut)

        self.setWindowTitle('SVG Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.show()

        self.loadSvg()

    def zoomIn(self):
        self.view.scale(1.2, 1.2)

    def zoomOut(self):
        self.view.scale(1 / 1.2, 1 / 1.2)

    def loadSvg(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "SVG files (*.svg)")
        if fname:
            self.renderer = QSvgRenderer(fname)
            self.scene.clear()
            self.scene.setSceneRect(self.renderer.viewBox().x(), self.renderer.viewBox().y(),
                                    self.renderer.viewBox().width(), self.renderer.viewBox().height())
            svg_item = QGraphicsSvgItem(fname)
            self.scene.addItem(svg_item)
            self.svg_data = self.extractSvgData(fname)

    @staticmethod
    def extractSvgData(fname):
        svg_data = {}
        try:
            tree = ElementTree.parse(fname)
            root = tree.getroot()
            for elem in root.iter():
                if 'id' in elem.attrib:
                    svg_data[elem.attrib['id']] = elem
        except Exception as e:
            logger.error(f"Error parsing SVG: {e}")
        return svg_data

    def setPipetteCursor(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.black)
        painter.drawEllipse(16, 16, 10, 10)
        painter.end()

        cursor = QCursor(pixmap, 16, 16)
        self.setCursor(cursor)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.setPipetteCursor()
            if event.buttons() == Qt.LeftButton:
                # Get the position of the mouse click in global coordinates
                global_pos = event.globalPos()
                # Map the global coordinates to coordinates in the QGraphicsView
                view_pos = self.view.mapFromGlobal(global_pos)
                # Map the view coordinates to scene coordinates
                scene_pos = self.view.mapToScene(view_pos)

                clicked_element_id = None

                for elem_id, elem in self.svg_data.items():
                    if elem.get('x') and elem.get('y'):
                        x = float(elem.get('x'))
                        y = float(elem.get('y'))
                        width = float(elem.get('width'))
                        height = float(elem.get('height'))
                        if x <= scene_pos.x() <= x + width and y <= scene_pos.y() <= y + height:
                            clicked_element_id = elem_id
                            break

                if clicked_element_id:
                    # Display the ID in a message box
                    QMessageBox.information(self, 'Element ID', f'Clicked on element with ID: {clicked_element_id}')
                    # Copy the ID to the clipboard
                    clipboard = QApplication.clipboard()
                    mime_data = QMimeData()
                    mime_data.setText(clicked_element_id)
                    clipboard.setMimeData(mime_data)
                else:
                    # Display a warning message
                    QMessageBox.warning(self, 'No Element ID', 'Clicked on an element with no ID')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SVGViewer()
    sys.exit(app.exec_())