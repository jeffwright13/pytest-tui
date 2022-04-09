from pytest_fold.utils import OUTCOMES, Results

import TermTk as ttk


class TkTui:
    def __init__(self) -> None:
        self.test_results = Results()
        self.summary_results = (
            self.test_results.Sections["LAST_LINE"]
            .content.replace("=", "")
            .replace("\n", "")
        )

        # Create root TTk object
        self.root = ttk.TTk(layout=ttk.TTkGridLayout())

    def create_top_frame(self) -> None:
        self.top_frame = ttk.TTkFrame(
            border=True,
            layout=ttk.TTkHBoxLayout(),
        )
        self.top_label = ttk.TTkLabel(
            parent=self.top_frame, text=ttk.TTkString(self.summary_results)
        )
        self.root.layout().addWidget(self.top_frame, 0, 0)

    def create_quit_button(self) -> None:
        self.quit_button = ttk.TTkButton(text="Quit", border=True, maxSize=(6, 3))
        self.quit_button.clicked.connect(self.root.quit)
        self.root.layout().addWidget(self.quit_button, 0, 1)

    def create_tab_widget(self) -> None:
        # Create tabs with results from individual sections
        self.tab_widget = ttk.TTkTabWidget(border=False)
        # self.tab_widget.setPadding(3, 0, 0, 0)
        self.root.layout().addWidget(self.tab_widget, 1, 0, 1, 2)

    def create_section_tabs(self) -> None:
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

        # text = self.test_results.Sections["PASSES_SECTION"].content
        # tab_label = "Passes Section"
        # text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        # text_area.setText(text)
        # text_areas[tab_label] = text_area
        # self.tab_widget.addTab(text_area, f"  {tab_label}")

        # text = self.test_results.Sections["FAILURES_SECTION"].content
        # tab_label = "Failures Section"
        # text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        # text_area.setText(text)
        # text_areas[tab_label] = text_area
        # self.tab_widget.addTab(text_area, f"  {tab_label}")

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

    def create_test_result_tabs(self) -> None:
        # Create tabs with results from individual sections

        for outcome in OUTCOMES:
            tab_label = outcome

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

            width = 10
            for result in eval(f"self.test_results.tests_{outcome.lower()}"):
                results_list.addItem(result)
                results_list.textClicked.connect(callback)
                width = max(width, len(result))

            results_splitter = ttk.TTkSplitter()
            results_splitter.addWidget(results_list, width)
            results_splitter.addWidget(results_view)

            self.tab_widget.addTab(results_splitter, f"  {tab_label}  ")


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
