from typing import Dict
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import (
    ScrollView,
    TreeClick,
)
from pytest_tui._tree_control import TreeControl
from pytest_tui.utils import Results


TREE_WIDTH = 120
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


class Tab(Widget):
    def __init__(
        self,
        label: str,
        style: str,
        content_type: str,  # either 'section' or 'tree'
    ) -> None:
        super().__init__()
        self.label = label
        self.content_type = content_type
        self.rich_text = Text(label, style=style)


class Tabs(Widget):
    def __init__(
        self,
        tabs: Dict[str, Tab],
    ) -> None:
        super().__init__()
        self.tabs = tabs

    async def action_clicked_tab(self, label: str) -> None:
        # Handle tabs being clicked
        if label == "Quit":
            quit()

        body = self.parent.parent.body
        test_results = self.parent.parent.test_results
        section_content = {
            "Summary": test_results.Sections["LAST_LINE"].content
            + test_results.Sections["TEST_SESSION_STARTS"].content
            + test_results.Sections["SHORT_TEST_SUMMARY"].content,
            "Warnings": test_results.Sections["WARNINGS_SUMMARY"].content,
            "Errors": test_results.Sections["ERRORS_SECTION"].content,
            "Full Output": test_results.unmarked_output,
        }
        tree_names = {
            "Passes": "pass_tree",
            "Failures": "fail_tree",
            "Skipped": "skip_tree",
            "Xfails": "xfail_tree",
            "Xpasses": "xpass_tree",
        }

        # Render the clicked tab with bold underline
        for tab_name in self.tabs:
            if tab_name == label:
                self.tabs[tab_name].rich_text.stylize("bold underline")
            else:
                self.tabs[tab_name].rich_text.stylize("not bold not underline")
            self.refresh()

        # Render section info
        if self.tabs[label].content_type == "section":
            self.parent.parent.body.visible = True
            await body.update(Text.from_ansi(section_content[label]))
        # Render tree info
        elif self.tabs[label].content_type == "tree":
            self.parent.parent.view.refresh()
            self.tree_name = tree_names[label]
            await body.update(eval(f"self.parent.parent.{self.tree_name}"))

    def render(self) -> RenderableType:
        # Build up renderable Text instance from a series of Tabs;
        # this simulates a tabbed widget as a workaround until Textual's
        # Tabs object has been released
        text = Text()
        text.append("│ ")
        for tab_name in self.tabs:
            text.append(self.tabs[tab_name].rich_text)
            text.append(" │ ")
            self.tabs[tab_name].rich_text.on(click=f"clicked_tab('{tab_name}')")
        return Panel(text, height=3)


class TuiApp(App):
    async def on_load(self, event: events.Load) -> None:
        # Get test result sections
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        tabs = {
            "Summary": Tab("Summary", "cyan bold underline", content_type="section"),
            "Passes": Tab("Passes", "green", content_type="tree"),
            "Failures": Tab("Failures", "red", content_type="tree"),
            "Skipped": Tab("Skipped", "yellow", content_type="tree"),
            "Xfails": Tab("Xfails", "yellow", content_type="tree"),
            "Xpasses": Tab("Xpasses", "yellow", content_type="tree"),
            "Warnings": Tab("Warnings", "yellow", content_type="section"),
            "Errors": Tab("Errors", "magenta", content_type="section"),
            "Full Output": Tab("Full Output", "cyan", content_type="section"),
            "Quit": Tab("Quit (Q)", "white", content_type="quit"),
        }
        self.tabs = Tabs(tabs)
        await self.view.dock(self.tabs, edge="top", size=3)

        # Body (to display result sections or result trees)
        self.body = ScrollView(
            Text.from_ansi(
                self.test_results.Sections["LAST_LINE"].content
                + self.test_results.Sections["TEST_SESSION_STARTS"].content
                + self.test_results.Sections["SHORT_TEST_SUMMARY"].content
            ),
            auto_width=True,
        )
        await self.view.dock(self.body)

        # Define the results trees
        self.fail_tree = TreeControl(
            Text("Failures:", style="bold red underline"),
            {"results": self.test_results.Sections["FAILURES_SECTION"].content},
            name="fail_tree",
        )
        self.pass_tree = TreeControl(
            Text("Passes:", style="bold green underline"), {}, name="pass_tree"
        )
        self.error_tree = TreeControl(
            Text("Errors:", style="bold magenta underline"), {}, name="error_tree"
        )
        self.skip_tree = TreeControl(
            Text("Skipped:", style="bold yellow underline"), {}, name="skip_tree"
        )
        self.xpass_tree = TreeControl(
            Text("Xpasses:", style="bold yellow underline"), {}, name="xpass_tree"
        )
        self.xfail_tree = TreeControl(
            Text("Xfails:", style="bold yellow underline"), {}, name="xfail_tree"
        )
        for failed in self.test_results.tests_failures:
            await self.fail_tree.add(
                self.fail_tree.root.id,
                Text(failed),
                {"results": self.test_results.tests_failures},
            )
        for passed in self.test_results.tests_passes:
            await self.pass_tree.add(
                self.pass_tree.root.id,
                Text(passed),
                {"results": self.test_results.tests_passes},
            )
        for errored in self.test_results.tests_errors:
            await self.error_tree.add(
                self.error_tree.root.id,
                Text(errored),
                {"results": self.test_results.tests_errors},
            )
        for skipped in self.test_results.tests_skipped:
            await self.skip_tree.add(
                self.skip_tree.root.id,
                Text(skipped),
                {"results": self.test_results.tests_skipped},
            )
        for xpassed in self.test_results.tests_xpasses:
            await self.xpass_tree.add(
                self.xpass_tree.root.id,
                Text(xpassed),
                {"results": self.test_results.tests_xpasses},
            )
        for xfailed in self.test_results.tests_xfails:
            await self.xfail_tree.add(
                self.xfail_tree.root.id,
                Text(xfailed),
                {"results": self.test_results.tests_xfails},
            )

        await self.fail_tree.root.expand()
        await self.pass_tree.root.expand()
        await self.error_tree.root.expand()
        await self.skip_tree.root.expand()
        await self.xpass_tree.root.expand()
        await self.xfail_tree.root.expand()

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when category header is clicked;
        # but don't try processing the category titles
        label = message.node.label
        if label.plain.upper().rstrip(":") in CATEGORIES:
            return
        for category in CATEGORIES:
            try:
                test_category = f"tests_{category.lower()}"
                self.text = eval(
                    f"self.test_results.{test_category}[message.node.label.plain]"
                )
            except Exception:
                pass

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = TuiApp()
    app.run()


if __name__ == "__main__":
    main()
