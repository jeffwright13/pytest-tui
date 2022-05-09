from tkinter import *
from tkinter.constants import END
from tkinter import ttk
from tkinter import scrolledtext
from pytest_tui.utils import Results
from rich.text import Text as richText
from strip_ansi import strip_ansi


def get_summary_results(results: Results) -> str:
    return results.Sections["LAST_LINE"].content.replace("=", "")


class TkApp:
    def __init__(self, root) -> None:
        self.root = root
        self.test_results = Results()
        self.root.title("pytest gui")

        self.mainframe = ttk.Frame(self.root, padding="3 3 6 6")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        summary_results = ttk.Label(
            self.mainframe,
            text=strip_ansi(get_summary_results(self.test_results))
        ).grid(column=0, row=0, sticky=(W, E))

        quit_button = ttk.Button(self.mainframe, text="Quit", command=self.mainframe.quit).grid(
            column=1, row=0, sticky=W
        )

    def create_notebook(self) -> None:
        def treeClicked(selection) -> None:
            print(f"Selection: {selection}")
            for selected_item in tree.selection():
                item = tree.item(selected_item)
            print("")

        def selectItem(a):
            curItem = tree.focus()
            print (tree.item(curItem))

            rich_text = richText.from_ansi(self.test_results.Sections["TEST_SESSION_STARTS"].content.split("\n")[0])

        self.notebook = ttk.Notebook(self.mainframe)

        width = len(self.test_results.Sections["TEST_SESSION_STARTS"].content.split("\n")[0])
        height = 60
        self.tab_frame_summary = ttk.Frame(self.notebook)
        stext = scrolledtext.ScrolledText(self.tab_frame_summary, width=width, height=height)
        stext.insert(END, strip_ansi(self.test_results.Sections["TEST_SESSION_STARTS"].content + self.test_results.Sections["SHORT_TEST_SUMMARY"].content))
        stext.pack(fill=BOTH, side=LEFT, expand=True)

        self.tab_frame_passes = ttk.Frame(self.notebook)
        tree = ttk.Treeview(self.tab_frame_passes)
        # tree["columns"] = ("test_title", "test_traceback")
        id = tree.insert('', 'end', 'passes', text='Passes')
        for passed in self.test_results.tests_passes:
            tree.insert("passes", "end", text=passed)
        tree.bind("<ButtonRelease-1>", treeClicked)
        # tree.bind("<ButtonRelease-1>", self.treeClicked(tree.selection()))
        # tree.bind("<ButtonRelease-1>", selectItem)
        tree.pack(fill=BOTH, side=LEFT)

        self.tab_frame_fails = ttk.Frame(self.notebook)
        tree = ttk.Treeview(self.tab_frame_fails)
        tree.insert('', 'end', 'fails', text='Fails')
        for failed in self.test_results.tests_failures:
            tree.insert("fails", "end", text=failed)
        tree.pack(fill=BOTH, side=LEFT)

        self.tab_frame_skipped = ttk.Frame(self.notebook)
        tree = ttk.Treeview(self.tab_frame_skipped)
        tree.insert('', 'end', 'skipped', text='Skipped')
        for skipped in self.test_results.tests_skipped:
            tree.insert("skipped", "end", text=skipped)
        tree.pack(fill=BOTH, side=LEFT)

        self.tab_frame_xfails = ttk.Frame(self.notebook)
        tree = ttk.Treeview(self.tab_frame_xfails)
        tree.insert('', 'end', 'xfails', text='Xfails')
        for xfailed in self.test_results.tests_xfails:
            tree.insert("xfails", "end", text=xfailed)
        tree.pack(fill=BOTH, side=LEFT)

        self.tab_frame_xpasses = ttk.Frame(self.notebook)
        tree = ttk.Treeview(self.tab_frame_xpasses)
        tree.insert('', 'end', 'xpasses', text='Xpasses')
        for xpassed in self.test_results.tests_xpasses:
            tree.insert("xpasses", "end", text=xpassed)
        tree.pack(fill=BOTH, side=LEFT)

        width = len(self.test_results.Sections["WARNINGS_SUMMARY"].content.split("\n")[0])
        self.tab_frame_warnings = ttk.Frame(self.notebook)
        stext = scrolledtext.ScrolledText(self.tab_frame_warnings)
        stext.insert(END, strip_ansi(self.test_results.Sections["WARNINGS_SUMMARY"].content))
        stext.pack(fill=BOTH, side=LEFT, expand=True)

        width = len(self.test_results.Sections["ERRORS_SECTION"].content.split("\n")[0])
        self.tab_frame_errors = ttk.Frame(self.notebook)
        stext = scrolledtext.ScrolledText(self.tab_frame_errors)
        stext.insert(END, strip_ansi(self.test_results.Sections["ERRORS_SECTION"].content))
        stext.pack(fill=BOTH, side=LEFT, expand=True)

        width = len(self.test_results.Sections["TEST_SESSION_STARTS"].content.split("\n")[0])
        self.tab_frame_full = ttk.Frame(self.notebook)
        stext = scrolledtext.ScrolledText(self.tab_frame_full)
        stext.insert(END, strip_ansi(self.test_results.unmarked_output))
        stext.pack(fill=BOTH, side=LEFT, expand=True)


        self.tab_frame_summary.pack(fill='both', expand=True)
        self.tab_frame_passes.pack(fill='both', expand=True)
        self.tab_frame_fails.pack(fill='both', expand=True)
        self.tab_frame_skipped.pack(fill='both', expand=True)
        self.tab_frame_xfails.pack(fill='both', expand=True)
        self.tab_frame_xpasses.pack(fill='both', expand=True)
        self.tab_frame_warnings.pack(fill='both', expand=True)
        self.tab_frame_errors.pack(fill='both', expand=True)
        self.tab_frame_full.pack(fill='both', expand=True)

        self.notebook.add(self.tab_frame_summary, text="Summary")
        self.notebook.add(self.tab_frame_passes, text="Passes")
        self.notebook.add(self.tab_frame_fails, text="Fails")
        self.notebook.add(self.tab_frame_skipped, text="Skipped")
        self.notebook.add(self.tab_frame_xfails, text="Xfails")
        self.notebook.add(self.tab_frame_xpasses, text="Xpasses")
        self.notebook.add(self.tab_frame_warnings, text="Warnings")
        self.notebook.add(self.tab_frame_errors, text="Errors")
        self.notebook.add(self.tab_frame_full, text="Full Output")

        self.notebook.enable_traversal()
        self.notebook.grid(
            column=0, row=1, sticky=(N, W, E, S)
        )


    def packit(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # self.root.update()


def main():
    root = Tk()
    tk_app = TkApp(root)
    tk_app.create_notebook()
    tk_app.packit()
    root.mainloop()


if __name__ == "__main__":
    main()
