from __future__ import annotations
from pytermgui.parser import MarkupLanguage as ML
from pytest_tui.utils import Results
import pytermgui as ptg

def _get_summary_results() -> str:
    test_results = Results()
    return test_results.Sections["LAST_LINE"].content.replace("=", "").replace("\n", "")

def _configure_widgets() -> None:
    """Defines all the global widget configurations.

    Some example lines you could use here:

        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)


def _define_layout() -> ptg.Layout:
    """Defines the application layout.

    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=3)
    layout.add_slot("Header right", width=0.12)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body")
    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=1)

    return layout


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _configure_widgets()
    summary_results = _get_summary_results()

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            ML().get_markup(summary_results),
            box="SINGLE",
            is_persistent=True
        )
        quitter = ptg.Window(ptg.Button("Quit (q)", lambda *_: manager.stop()), box="SINGLE", is_persistent=True)

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)
        manager.add(quitter)


        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"

        manager.add(ptg.Window("My body window"), assign="body")

    ptg.tim.print("[!gradient(210)]Goodbye!")


if __name__ == "__main__":
    main()
