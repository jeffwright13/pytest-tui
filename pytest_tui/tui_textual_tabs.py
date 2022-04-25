from typing import TypedDict, Dict
from rich.console import RenderableType
from rich.style import Style
from rich.text import Text
from textual import events
from textual.app import App
from textual import messages
from textual.views import DockView
from textual.widget import Widget
from textual.widgets import (
    Header,
    Footer,
    TreeControl,
    ScrollView,
    TreeClick,
    Placeholder,
)
from pytest_tui.utils import Results


class TuiFooter(Footer):
    # Override default Footer method 'make_key_text' to allow customizations
    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style="bold white on black",
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


# class Tab(Widget):
#     def __init__(
#         self,
#         label: Union[str, Text],
#         style: Style,
#         content_type: Union[ScrollView, TreeControl],
#     ) -> None:
#         super().__init__()
#         self.label = label
#         self.style = style
#         self.content_type = content_type
#         self.rich_text = Text(label, style=style)


class TabLabel:
    name: str
    style: str


class Tab(Widget):
    def __init__(
        self,
        # label: TabLabel,
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
        self.view = DockView()

    async def action_clicked_tab(self, label: str) -> None:
        for tab_name in self.tabs:
            if tab_name == label:
                self.tabs[tab_name].rich_text.stylize("bold underline")
            else:
                self.tabs[tab_name].rich_text.stylize("not bold not underline")
        self.refresh()
        await self.view.dock()

    def render(self):
        text = Text()
        text.append("┊ ")
        for tab_name in self.tabs:
            # text.append(self.tabs[tab].rich_text).on(click=f"clicked_tab('{tab}')")
            text.append(self.tabs[tab_name].rich_text)
            text.append(" ┊ ")
            self.tabs[tab_name].rich_text.on(click=f"clicked_tab('{tab_name}')")
        return text


    # def render(self):
    #     text = Text()
    #     text.append("┊ ")
    #     text.append(Text("Summary").on(click="clicked_tab('Summary')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Passes").on(click="clicked_tab('Passes')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Failures").on(click="clicked_tab('Failures')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Skipped").on(click="clicked_tab('Skipped')"))
    #     text.append(" ┊ ")
    #     text.append(Text("XFails").on(click="clicked_tab('Xfails')"))
    #     text.append(" ┊ ")
    #     text.append(Text("XPasses").on(click="clicked_tab('Xpasses')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Warnings").on(click="clicked_tab('Warnings')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Errors").on(click="clicked_tab('Errors')"))
    #     text.append(" ┊ ")
    #     text.append(Text("Full Output").on(click="clicked_tab('Full')"))
    #     text.append(" ┊ ")
    #     return text


class TuiApp(App):
    async def on_load(self, event: events.Load) -> None:
        # Get test result sections
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        # Create and dock header widget
        self.title = self.summary_results
        self.header = Header(style="bold white on black", clock=False)
        self.header.title = self.summary_results
        await self.view.dock(self.header, edge="top", size=1)

        # Create and dock footer widget
        self.footer = TuiFooter()
        await self.view.dock(self.footer, edge="bottom")

        # Tabs
        # tabs = {
        #     "Summary": Tab(TabLabel("Summary", "cyan"), content_type="section"),
        #     "Passes": Tab(TabLabel("Passes", "green"), content_type="tree"),
        #     "Failures": Tab(TabLabel("Failures", "red"), content_type="tree"),
        #     "Skipped": Tab(TabLabel("Skipped", "yellow"), content_type="tree"),
        #     "XFails": Tab(TabLabel("XFails", "yellow"), content_type="tree"),
        #     "Xpasses": Tab(TabLabel("XPasses", "yellow"), content_type="tree"),
        #     "Warnings": Tab(TabLabel("Warnings", "yellow"), content_type="section"),
        #     "Errors": Tab(TabLabel("Errors", "magenta"), content_type="tree"),
        #     "Full Output": Tab(TabLabel("Full Output", "cyan"), content_type="section"),
        # }
        tabs = {
            "Summary": Tab("Summary", "cyan", content_type="section"),
            "Passes": Tab("Passes", "green", content_type="tree"),
            "Failures": Tab("Failures", "red", content_type="tree"),
            "Skipped": Tab("Skipped", "yellow", content_type="tree"),
            "XFails": Tab("XFails", "yellow", content_type="tree"),
            "Xpasses": Tab("XPasses", "yellow", content_type="tree"),
            "Warnings": Tab("Warnings", "yellow", content_type="section"),
            "Errors": Tab("Errors", "magenta", content_type="tree"),
            "Full Output": Tab("Full Output", "cyan", content_type="section"),
        }
        self.tabs = Tabs(tabs)
        await self.view.dock(self.tabs, edge="top", size=2)

        # Body (to display full sections or result trees)
        self.body = ScrollView(
            Text.from_ansi(self.test_results.Sections["TEST_SESSION_STARTS"].content)
        )
        await self.view.dock(self.body)


TuiApp.run()
