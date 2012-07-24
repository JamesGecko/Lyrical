@echo off
pyside-uic gui/mainwindow.ui > gui/ui_mainwindow.py
pyside-uic gui/projector.ui > gui/ui_projector.py
pyside-uic gui/editor.ui > gui/ui_editor.py
pyside-uic gui/picker.ui > gui/ui_picker.py
