@echo off
pyside-uic lyrical/gui/mainwindow.ui > lyrical/gui/ui_mainwindow.py
pyside-uic lyrical/gui/projector.ui > lyrical/gui/ui_projector.py
pyside-uic lyrical/gui/edit.ui > lyrical/gui/ui_editor.py
pyside-uic lyrical/gui/picker.ui > lyrical/gui/ui_picker.py
