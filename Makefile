main : mainwindow projector editor picker

projector : gui/ui_projector.py
	pyside-uic gui/projector.ui > gui/ui_projector.py

mainwindow : gui/mainwindow.ui
	pyside-uic gui/mainwindow.ui > gui/ui_mainwindow.py

editor : gui/ui_editor.py
	pyside-uic gui/edit.ui > gui/ui_editor.py

picker : gui/ui_picker.py
	pyside-uic gui/picker.ui > gui/ui_picker.py

