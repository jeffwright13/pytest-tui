import pickle
from pathlib import Path
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import OUTFILE, PICKLEFILE, sectionize

TREE_WIDTH = 30
SECTIONS = {
    "FIRSTLINE": "bold blue underline",
    "FAILURES": "bold red underline",
    "ERRORS": "bold magenta underline",
    "WARNINGS": "bold yellow underline",
    "SUMMARY": "bold green underline",
    "LAST_LINE": "bold blue underline",
}


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and sectionize the results into individual sections for
    display on the TUI. Relies on utils.py.
    """

    def __init__(
        self, results_file_path: Path = OUTFILE, pickle_file_path: Path = PICKLEFILE
    ) -> None:
        self.results_file = results_file_path
        self.pass_file = pickle_file_path
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

    def read_passes(self) -> None:
        with open(self.pass_file, "rb") as pass_file:
            passes = pickle.load(pass_file)
        return passes


class FoldFooter(Footer):
    # Override default Footer method 'make_key_text' to allow customizations
    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style="bold encircle white on black",
            no_wrap=True,
            overflow="ellipsis",
            justify="center",
            end="",
        )
        for binding in self.app.bindings.shown_keys:
            key_display = (
                binding.key.upper()
                if binding.key_display is None
                else binding.key_display
            )
            hovered = self.highlight_key == binding.key
            key_text = Text.assemble(
                (f" {key_display} ", "reverse" if hovered else "default on default"),
                f" {binding.description} ",
                meta={"@click": f"app.press('{binding.key}')", "key": binding.key},
            )
            text.append_text(key_text)
        return text


class FoldApp(App):
    """
    Textual class inherited from App
    Provides docking and data population for test session headers and results
    """

    async def on_load(self, event: events.Load) -> None:
        # Populate footer with quit and toggle info
        await self.bind("t", "view.toggle('results_tree')", "Toggle Results Tree  |")
        await self.bind("q", "quit", "Quit")

        # Load results from OUTFILE; bind actions to heaader/footer widgets
        results_data = ResultsData()
        self.results = results_data.get_results_dict()
        self.summary_text = (
            Text.from_ansi(self.results["LAST_LINE"]).markup.replace("=", "").strip()
        )

        # Load passed file results from PICKLEFILE
        self.passes = results_data.read_passes()

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        self.title = self.summary_text
        header1 = Header(tall=False, style="bold white on black underline")
        header1.title = self.summary_text
        await self.view.dock(header1, edge="top", size=1)
        footer = FoldFooter()
        await self.view.dock(footer, edge="bottom")

        # Stylize the results-tree section headers
        tree = TreeControl(Text("TEST RUN RESULTS:", style="bold white underline"), {})
        for results_key in self.results.keys():
            if results_key in ("LAST_LINE", "SUMMARY"):
                continue
            await tree.add(tree.root.id, Text(results_key), {"results": self.results})
            if tree.nodes[tree.id].label.plain == "FIRSTLINE":
                tree.nodes[tree.id].label.stylize("bold blue underline")
            elif tree.nodes[tree.id].label.plain == "FAILURES":
                tree.nodes[tree.id].label.stylize("bold red underline")
            elif tree.nodes[tree.id].label.plain == "ERRORS":
                tree.nodes[tree.id].label.stylize("bold magenta underline")
            elif tree.nodes[tree.id].label.plain == "WARNINGS":
                tree.nodes[tree.id].label.stylize("bold yellow underline")
            elif tree.nodes[tree.id].label.plain == "SUMMARY":
                tree.nodes[tree.id].label.stylize("bold green underline")
            else:
                tree.nodes[tree.id].label.stylize("encircle red")
        await tree.add(tree.root.id, Text("PASSES"), {})
        tree.nodes[tree.id].label.stylize("bold green underline")
        for item in self.passes:
            await tree.add(
                tree.root.id,
                Text(item.title),
                {
                    "item": {
                        "caplog": item.caplog,
                        "capstderr": item.capstderr,
                        "capstdout": item.capstdout,
                    }
                },
            )
            tree.nodes[tree.id].label.stylize("cyan")
        await tree.root.expand()

        # Create and dock the results tree
        self.sections = DockView()
        await self.view.dock(
            ScrollView(tree), edge="left", size=TREE_WIDTH, name="results_tree"
        )
        await self.view.dock(self.sections)

        # Create and dock the test result ('body') view
        self.body = ScrollView()
        await self.sections.dock(self.body, edge="top")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when section header is clicked
        label = message.node.label.plain
        if label in ("ERRORS", "FAILURES", "PASSES"):
            return
        try:
            self.text = message.node.data.get("results")[label]
        except TypeError:
            caplog = message.node.data.get("item")["caplog"]
            capstderr = message.node.data.get("item")["capstderr"]
            capstdout = message.node.data.get("item")["capstdout"]
            self.text = caplog + capstderr + capstdout
            if len(self.text) == 0:
                self.text = "<<no stdout, stderr, or stdlog output from this test>>"
        except Exception as e:
            return
        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    # Instantiate app and run it
    app = FoldApp()
    app.run()


if __name__ == "__main__":
    main()
