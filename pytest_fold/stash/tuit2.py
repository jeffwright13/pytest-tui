from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import OUTCOMES, Results


class PytestFoldApp(App):

    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")

        # Get test result sections
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        self.unmarked_output = self.test_results.unmarked_output
        self.marked_output = self.test_results.marked_output

    async def on_mount(self) -> None:
        header1 = Header(style="bold white on black")
        header1.title = self.summary_results
        await self.view.dock(header1, edge="top", size=1)

        self.body = ScrollView()
        self.dock_view = DockView()

        tree = TreeControl("pytest --fold", {})
        for results_key in OUTCOMES:
            await tree.add(tree.root.id, results_key, {"results": self.test_results.tests_failures})
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
