from __future__ import annotations
from collections import Counter
from pathlib import Path
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer
from textual.reactive import Reactive

from ck_widgets_lv import ListViewUo

from pytest_fold.utils import MARKERS, OUTFILE, sectionize


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and sectionize the results into individual sections for
    display on the TUI
    """

    def __init__(self, path: Path = OUTFILE) -> None:
        self.results_file = path
        self.sections = []
        self.parsed_sections = []

    def _sectionize_results(self) -> None:
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = sectionize(results_lines)

    def get_results(self) -> list:
        self._sectionize_results()
        return self.sections


class Hover(Widget):
    mouse_over = Reactive(False)
    folded = Reactive(False)

    def __init__(self, size: tuple = (0, 0), text: str = "") -> None:
        super().__init__(size)
        self.text = text
        self.panel = Panel(self.text)
        self.folded = True
        self.collapsed_size = 3
        self.full_size = Counter(self.text.plain)["\n"] + 5

    def render(self) -> Panel:
        return Panel(
            self.text,
            style=("italic" if not self.mouse_over else "bold"),
            height=self.collapsed_size if self.folded else self.full_size,
        )

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_click(self) -> None:
        self.folded = not (self.folded)

    def on_leave(self) -> None:
        self.mouse_over = False


class HoverApp(App):
    async def on_load(self, event: events.Load) -> None:
        await self.bind("t", "view.toggle('topbar')", "Pytest Fold")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top", size=1)
        await self.view.dock(Footer(), edge="bottom")

        sections = ResultsData().get_results()
        hovers = [
            Hover(text=Text.from_ansi(section["content"])) for section in sections
        ]
        await self.view.dock(ListViewUo(widgets=hovers, edge="top"))


def main():
    HoverApp.run(log="textual.log")
    # HoverApp.run(css_file="tuit.css", watch_css=True, log="textual.log")


if __name__ == "__main__":
    main()
#
