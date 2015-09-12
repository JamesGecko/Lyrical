from PySide.QtCore import Qt
from PySide.QtGui import QWidget
from gui.ui_projector import Ui_Projector

class LyricalProjector(QWidget, Ui_Projector):
    def __init__(self):
        QWidget.__init__(self)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setupUi(self)
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

