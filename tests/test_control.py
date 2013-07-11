import unittest
import sys
from PySide.QtTest import QTest
from PySide.QtCore import Qt
from PySide.QtGui import QApplication
from .context import lyrical

class Test_LyricalControl(unittest.TestCase):
    def setUp(self):
        self.db = lyrical.model.Database(':memory:')
        self.db.create_tables()
        self.app = QApplication(sys.argv)
        self.projector = lyrical.LyricalProjector()
        self.controller = lyrical.LyricalControl(self.projector, self.db)

    def test_clicking_picker_button_opens_picker_window(self):
        QTest.mouseClick(self.controller.add_button, Qt.LeftButton)
        picker_window_open = False
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, lyrical.LyricalPicker):
                picker_window_open = True
        self.assertTrue(picker_window_open)
