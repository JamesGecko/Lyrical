from PySide.QtCore import Qt
from PySide.QtGui import QWidget
from PySide.QtGui import QDesktopWidget
from gui.ui_projector import Ui_Projector

class LyricalProjector(QWidget, Ui_Projector):
    def __init__(self, screen_number):
        QWidget.__init__(self)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setupUi(self)
        self.setWindowTitle('Projector Screen')
        self._assignToScreen(screen_number)
        self.controller = None
        self.style = '''
        color: white;
        background-color: black;
        padding-top: 20px;
        padding-left: 20px;
        font-size: 40px;
        text-align: center;
        ''' #TODO: text-align doesn't work with QTextBrowser widgets
        self.content.setStyleSheet(self.style)

    def _assignToScreen(self, screen_number):
        coords = QDesktopWidget().screenGeometry(screen_number)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(coords.topLeft())
        self.resize(coords.size())
        self.showFullScreen()


    def update(self, slide):
        '''set title and content to slide
        '''
        self.title.setText(slide.title)
        self.content.setText(slide.content)

    def focusInEvent(self, event):
        '''When focused, set the focus back to the control window.
        '''
        if not self.controller:
            raise 'Controller not set'
        self.controller.raise_()
        self.controller.activateWindow()

