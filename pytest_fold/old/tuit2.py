import re
from pathlib import Path

from rich.console import RenderableType
from rich.text import Text
from rich import print
from rich.panel import Panel
from rich.style import Style

from textual import events
from textual.app import App
from textual.reactive import Reactive

from textual.views import DockView
from textual.widgets import (
    Header,
    Footer,
    TreeControl,
    ScrollView,
    TreeClick,
    Placeholder,
)

from pytest_fold.utils import MARKERS, OUTFILE, sectionize


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and sectionize the results into individual sections for
    display on the TUI. Relies on utils.py.
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

    def get_results_dict(self) -> dict:
        self.results = self.get_results()
        d = {}
        for section in self.results:
            if section["test_title"]:
                d[section["test_title"]] = section["content"]
            else:
                d[section["name"]] = section["content"]
        return d


class PytestFoldApp(App):

    results = ResultsData().get_results_dict()

    async def on_load(self, event: events.Load) -> None:
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        footer_title = re.sub("=", "", self.results["LASTLINE"])
        await self.view.dock(Header(tall=False), edge="top", size=1)
        await self.view.dock(Footer(), edge="bottom")

        self.body = ScrollView()
        self.dock_view = DockView()
        self.placeholder = Placeholder()

        tree = TreeControl("pytest --fold", {})
        for results_key in self.results.keys():
            await tree.add(tree.root.id, results_key, {"results": self.results})
        await tree.root.expand()

        await self.view.dock(ScrollView(tree), edge="left", size=48, name="sidebar")
        await self.view.dock(self.dock_view)
        await self.dock_view.dock(self.body, edge="top", size=48)

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        """Called in response to a tree click."""
        label = self.text = message.node.label
        self.text = message.node.data.get("results")[label]

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    PytestFoldApp(title="pytest --fold results").run()


if __name__ == "__main__":
    main()
