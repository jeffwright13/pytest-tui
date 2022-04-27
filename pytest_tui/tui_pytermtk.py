import TermTk as ttk

from pytest_tui.utils import OUTCOMES, Results


class TkTui:
    def __init__(self) -> None:
        # Instantiate pytest-tui's Results object, and populate w/ data
        self.test_results = Results()
        self.summary_results = (
            self.test_results.Sections["LAST_LINE"]
            .content.replace("=", "")
            .replace("\n", "")
        )

        # Create root TTk object
        self.root = ttk.TTk(layout=ttk.TTkGridLayout())

    def create_top_frame(self) -> None:
        # top frame holds test run summary statistics, colorized
        self.top_frame = ttk.TTkFrame(
            border=True,
            layout=ttk.TTkHBoxLayout(),
        )
        self.top_label = ttk.TTkLabel(
            parent=self.top_frame, text=ttk.TTkString(self.summary_results)
        )
        self.root.layout().addWidget(self.top_frame, 0, 0)

    def create_quit_button(self) -> None:
        # callback for Quit button
        self.quit_button = ttk.TTkButton(text="Quit", border=True, maxSize=(6, 3))
        self.quit_button.clicked.connect(self.root.quit)
        self.root.layout().addWidget(self.quit_button, 0, 1)

    def keyPressEvent(self, evt) -> bool:
        # Handle keypress 'Q'
        if evt.key == ttk.TTkK.Key_Q:
            self.root.quit()
        return False

    def keyEvent(self, evt):
        if evt.type == ttk.TTkK.Character and evt.key == ttk.TTkK.Key_Q:
            self.root.quit()

    def create_tab_widget(self) -> None:
        # Create tabs for results from individual terminal output sections
        self.tab_widget = ttk.TTkTabWidget(border=False)
        self.root.layout().addWidget(self.tab_widget, 1, 0, 1, 2)

    def create_test_result_tabs(self) -> None:
        # Create tabs with results from individual tests, per outcome category
        for outcome in OUTCOMES:

            # We already show ERRORS section in its entirety; no sense in itemizing it
            if outcome in ("Errors"):
                continue

            results_list = ttk.TTkList()
            results_view = ttk.TTkTextEdit()
            results_view.setLineWrapMode(ttk.TTkK.WidgetWidth)
            results_view.setWordWrapMode(ttk.TTkK.WrapAnywhere)

            @ttk.pyTTkSlot(str)
            def callback(
                test_name: str, rlist=results_list, rview=results_view
            ) -> None:
                ttk.TTkLog.info(f"Clicked test: {test_name}")
                rview.clear()
                for label in rlist.selectedLabels():
                    rview.append(self.test_results.tests_all[label])

            min_width = 30
            max_width = 60
            for result in eval(f"self.test_results.tests_{outcome.lower()}"):
                results_list.addItem(result)
                results_list.textClicked.connect(callback)
                width = max(min_width, min(max_width, len(result)))

            results_splitter = ttk.TTkSplitter()
            results_splitter.addWidget(results_list, width)
            results_splitter.addWidget(results_view)

            tab_label = outcome
            self.tab_widget.addTab(results_splitter, f"  {tab_label}  ")

    def create_section_tabs(self) -> None:
        # Create tabs with results from individual terminal output sections
        text = (
            self.test_results.Sections["TEST_SESSION_STARTS"].content
            + self.test_results.Sections["SHORT_TEST_SUMMARY"].content
        )
        tab_label = "Summary"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        # text_area.lineWrapMode == TTkK.WidgetWidth
        text_area.setText(text)
        text_areas = {tab_label: text_area}
        self.tab_widget.addTab(text_area, f"  {tab_label}  ")

        text = self.test_results.unmarked_output
        tab_label = "Full Output"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_areas[tab_label] = text_area
        text_area.setText(text)
        self.tab_widget.addTab(text_area, f"  {tab_label}  ")

        text = self.test_results.Sections["ERRORS_SECTION"].content
        tab_label = "Errors"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f"  {tab_label}  ")

        text = self.test_results.Sections["WARNINGS_SUMMARY"].content
        tab_label = "Warnings"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f"  {tab_label}  ")


def main():
    tui = TkTui()

    tui.create_top_frame()
    tui.create_quit_button()
    tui.create_tab_widget()
    tui.create_section_tabs()
    tui.create_test_result_tabs()

    tui.root.mainloop()


if __name__ == "__main__":
    main()
