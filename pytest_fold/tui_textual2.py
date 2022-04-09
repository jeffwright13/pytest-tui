from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import Results

TREE_WIDTH = 30

SECTIONS = {
    "PASSES": "bold green underline",
    "FAILURES": "bold red underline",
    "ERRORS": "bold magenta underline",
    "WARNINGS_SUMMARY": "bold yellow underline",
}

CATEGORIES = {
    "PASSES": "bold green underline",
    "FAILURES": "bold red underline",
    "ERRORS": "bold magenta underline",
    "SKIPPED": "bold cyan underline",
    "XFAILS": "bold indian_red underline",
    "XPASSES": "bold chartreuse1 underline",
}


class PytestFoldApp(App):
    async def on_load(self, event: events.Load) -> None:
        # Load results from OUTFILE; bind actions to heaader/footer widgets
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        self.unmarked_output = self.test_results.unmarked_output
        self.marked_output = self.test_results.marked_output
        await self.bind("b", "view.toggle('sidebar')", "Toggle Tree")
        await self.bind("q", "quit", "Quit")
        await self.bind("~", None, f"{self.summary_results}")

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        header = Header(style="bold white on black")
        header.title = self.summary_results
        await self.view.dock(header, edge="top", size=1)

        footer = Footer()
        await self.view.dock(footer, edge="bottom")

        tree = TreeControl("TEST RESULTS:", {})

        for category in CATEGORIES:
            category_text = Text(category)
            category_text.stylize(CATEGORIES[category])
            await tree.add(
                tree.root.id,
                category_text,
                {"results": eval(f"self.test_results.tests_{category.lower()}")},
            )
            for testname in eval(f"self.test_results.tests_{category.lower()}"):
                _test_text = Text(testname)
                _test_text.stylize("italic")
                await tree.add(tree.root.id, _test_text, {})

        await tree.root.expand()

        # Create and dock the results header tree, and individual results
        self.body = ScrollView()
        self.dock_view = DockView()
        await self.view.dock(
            ScrollView(tree), edge="left", size=TREE_WIDTH, name="sidebar"
        )
        await self.view.dock(self.dock_view)
        await self.dock_view.dock(self.body, edge="top")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when category header is clicked;
        # but don't try processing the category titles
        label = message.node.label
        if label.plain in CATEGORIES:
            return

        for category in CATEGORIES:
            try:
                test_category = f"tests_{category.lower()}"
                self.text = eval(
                    f"self.test_results.{test_category}[message.node.label.plain]"
                )
            except:
                pass

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = PytestFoldApp()
    app.run()


if __name__ == "__main__":
    main()
