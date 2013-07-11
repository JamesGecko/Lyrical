class Slide(object):
    def __init__(self, title, content):
        self.title = title
        self.content = self.convert_line_breaks(content)

    def convert_line_breaks(self, text):
        return text.replace('\n', '<br>')

