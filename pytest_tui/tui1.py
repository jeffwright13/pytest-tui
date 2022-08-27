from sys import exit
from typing import Dict

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import ScrollView, TreeClick

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
        results = self.parent.parent.results
        section_content = {
            "Summary": results.tui_sections.lastline.content
            + results.tui_sections.test_session_starts.content
            + results.tui_sections.short_test_summary.content,
            "Warnings": results.tui_sections.warnings_summary.content,
            "Errors": results.tui_sections.errors.content,
            "Full Output": results.terminal_output,
        }
        tree_names = {
            "Passes": "passes_tree",
            "Failures": "failures_tree",
            "Skipped": "skipped_tree",
            "Xfails": "xfails_tree",
            "Xpasses": "xpasses_tree",
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
        self.results = Results()
        if not self.results.tui_sections and self.results.tui_test_results:
            exit()
        self.summary_results = self.results.tui_sections.lastline.content.replace(
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
                self.results.tui_sections.lastline.content
                + self.results.tui_sections.test_session_starts.content
                + self.results.tui_sections.short_test_summary.content
            ),
            auto_width=True,
        )
        await self.view.dock(self.body)

        # Define the results trees
        self.failures_tree = TreeControl(
            Text("Failures:", style="bold red underline"),
            {},
            name="failures_tree",
        )
        self.passes_tree = TreeControl(
            Text("Passes:", style="bold green underline"), {}, name="passes_tree"
        )
        self.errors_tree = TreeControl(
            Text("Errors:", style="bold magenta underline"), {}, name="errors_tree"
        )
        self.skipped_tree = TreeControl(
            Text("Skipped:", style="bold yellow underline"), {}, name="skipped_tree"
        )
        self.xpasses_tree = TreeControl(
            Text("Xpasses:", style="bold yellow underline"), {}, name="xpasses_tree"
        )
        self.xfails_tree = TreeControl(
            Text("Xfails:", style="bold yellow underline"), {}, name="xfails_tree"
        )
        for failed in self.results.tui_test_results.all_failures():
            await self.failures_tree.add(
                self.failures_tree.root.id,
                Text(failed.fqtn),
                {"results": f"{failed.caplog}{failed.capstderr}{failed.capstdout}"},
            )
        for passed in self.results.tui_test_results.all_passes():
            await self.passes_tree.add(
                self.passes_tree.root.id,
                Text(passed.fqtn),
                {"results": f"{passed.caplog}{passed.capstderr}{passed.capstdout}"},
            )
        for errored in self.results.tui_test_results.all_errors():
            await self.errors_tree.add(
                self.errors_tree.root.id,
                Text(errored.fqtn),
                {"results": f"{errored.caplog}{errored.capstderr}{errored.capstdout}"},
            )
        for skipped in self.results.tui_test_results.all_skipped():
            await self.skipped_tree.add(
                self.skipped_tree.root.id,
                Text(skipped.fqtn),
                {"results": f"{skipped.caplog}{skipped.capstderr}{skipped.capstdout}"},
            )
        for xpassed in self.results.tui_test_results.all_xpasses():
            await self.xpasses_tree.add(
                self.xpasses_tree.root.id,
                Text(xpassed.fqtn),
                {"results": f"{xpassed.caplog}{xpassed.capstderr}{xpassed.capstdout}"},
            )
        for xfailed in self.results.tui_test_results.all_xfails():
            await self.xfails_tree.add(
                self.xfails_tree.root.id,
                Text(xfailed.fqtn),
                {"results": f"{xfailed.caplog}{xfailed.capstderr}{xfailed.capstdout}"},
            )

        await self.failures_tree.root.expand()
        await self.passes_tree.root.expand()
        await self.errors_tree.root.expand()
        await self.skipped_tree.root.expand()
        await self.xpasses_tree.root.expand()
        await self.xfails_tree.root.expand()

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when category header is clicked;
        # but don't try processing the category titles
        label = message.node.label
        if label.plain.upper().rstrip(":") in CATEGORIES:
            return
        category = message.sender.name.rstrip("_tree")
        all_tests_in_category = eval(
            f"self.results.tui_test_results.all_{category.lower()}()"
        )
        for test in all_tests_in_category:
            if test.fqtn == label.plain:
                self.text = Text.from_ansi(
                    f"{test.caplog}{test.capstderr}{test.capstdout}"
                )
                break

        await self.body.update(self.text.markup)


def main():
    app = TuiApp()
    app.run()


if __name__ == "__main__":
    main()
