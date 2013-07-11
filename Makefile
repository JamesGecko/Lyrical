main : mainwindow projector editor picker

projector : lyrical/gui/ui_projector.py
	pyside-uic lyrical/gui/projector.ui > lyrical/gui/ui_projector.py

mainwindow : lyrical/gui/mainwindow.ui
	pyside-uic lyrical/gui/mainwindow.ui > lyrical/gui/ui_mainwindow.py

editor : lyrical/gui/ui_editor.py
	pyside-uic lyrical/gui/edit.ui > lyrical/gui/ui_editor.py

picker : lyrical/gui/ui_picker.py
	pyside-uic lyrical/gui/picker.ui > lyrical/gui/ui_picker.py

