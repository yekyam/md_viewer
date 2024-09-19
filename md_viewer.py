import sys
from typing import Iterable

from textual.app import App, ComposeResult, SystemCommand
from textual.widgets import Header, Footer, Button, ContentSwitcher, MarkdownViewer, Static, TextArea, Markdown
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen


def read_lines_from_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

class MarkdownViewerApp(App):
    """A textual app to view and edit markdown files."""

    CSS_PATH = "content_switcher.tcss"
    text = reactive('')
    editing = False

    #    BINDINGS = [('tab', 'toggle_view', "Toggle between editor and viewer")]
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand("Save", "Save the markdown to the file", self.save)

    def save(self):
        with open(self.outfile, "w") as f:
            f.write(self.query_one(TextArea).text)

    def on_text_area_changed(self, event) -> None:
        text = self.query_one(TextArea).text
        self.query_one(Markdown).update(text)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()

        with Horizontal(id="buttons"):
            yield Button("Viewer", id='viewer')
            yield Button("Editor", id='editor')

        with ContentSwitcher(initial='viewer'):
            yield TextArea(self.text, id='editor')
            with VerticalScroll(id='viewer'):
                yield MarkdownViewer(self.text)

        yield Footer()

def main():
    if len(sys.argv) != 2:
        print('usage; python mardown_viewer.py (filename)')
        return

    filename = sys.argv[1]
    text = ''
    try:
        lines = read_lines_from_file(filename)
        text = ''.join(lines)
    except Exception as e:
        print(f"Couldn't open file: {filename}")
        return

    app = MarkdownViewerApp()
    app.text = text
    app.outfile = filename
    app.run()

if __name__ == '__main__':
    main()
