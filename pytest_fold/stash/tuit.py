from pathlib import Path
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.views import DockView
from textual.widgets import Header, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import OUTFILE, sectionize, Results

TREE_WIDTH = 30
SECTIONS = {
    "FIRSTLINE": "bold blue underline",
    "FAILURES": "bold red underline",
    "ERRORS": "bold magenta underline",
    "WARNINGS_SUMMARY": "bold yellow underline",
    "TERMINAL_SUMMARY": "bold green underline",
    "LASTLINE": "bold blue underline",
}


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


class FoldApp(App):
    """
    Textual class inherited from App
    Provides docking and data population for test session headers and results
    """

    async def on_load(self, event: events.Load) -> None:
        # Load results from OUTFILE; bind actions to heaader/footer widgets
        self.results = ResultsData().get_results_dict()
        self.summary_text = (
            Text.from_ansi(self.results["LASTLINE"]).markup.replace("=", "").strip()
        )
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        self.title = self.summary_text
        header1 = Header(tall=False, style="white on black underline")
        header2 = Header(tall=False, style="white on black", clock = False)
        await self.view.dock(header1, edge="top", size=1)
        await self.view.dock(header2, edge="bottom", size=1)

        # Stylize the results-tree section headers
        tree = TreeControl("SESSION RESULTS:", {})
        for results_key in self.results.keys():
            await tree.add(tree.root.id, Text(results_key), {"results": self.results})
            for k, v in SECTIONS.items():
                if tree.nodes[tree.id].label.plain == k:
                    tree.nodes[tree.id].label.stylize(v)
                    continue
                else:
                    tree.nodes[tree.id].label.stylize("italic")
        await tree.root.expand()

        # Create and dock the results header tree, and individual results
        self.body = ScrollView()
        self.sections = DockView()
        await self.view.dock(
            ScrollView(tree), edge="left", size=TREE_WIDTH, name="sidebar"
        )
        await self.view.dock(self.sections)
        await self.sections.dock(self.body, edge="top")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when section header is clicked
        label = message.node.label
        self.text = message.node.data.get("results")[label._text[0]]
        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = FoldApp()
    app.run()


if __name__ == "__main__":
    main()
