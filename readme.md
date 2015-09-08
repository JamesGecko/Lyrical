#Lyrical

This is a simple application for projecting lyrics. It is intended to aid
churches in their worship services.

##Installation and use

- PySide is a major dependency, and it isn't available via pip.
Sorry, virtualenv users. [Get PySide](http://qt-project.org/wiki/Get-PySide).
- Then run `make` on UNIX-like systems, or `build.bat` on Windows.
- Execute `lyrical/app.py` to start the application.
- On first run, Lyrical will create an sqlite song database in `~/.lyrical`.

##Song file format

The import and export function (coming soon) allows you to store songs in
simple text files for theoretical easy migration between programs.
- The first line is the title.
- The second line is the copyright. If this line is blank, Lyrical will skip it.
- All following paragraphs are individual verses. Each one will recieve its own
slide.
