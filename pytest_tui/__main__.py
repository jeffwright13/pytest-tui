import configparser
import platform
import subprocess
import sys

from blessed import Terminal
from bullet import Bullet, Input, YesNo, colors
from rich import print

from pytest_tui.tui1 import main as tui1
from pytest_tui.tui2 import main as tui2
from pytest_tui.utils import CONFIGFILE


class DefaultConfig:
    HTML_LIGHT_THEME = {
        "BODY_FOREGROUND_COLOR": "000000",
        "BODY_BACKGROUND_COLOR": "EEEEEE",
        "INV_FOREGROUND_COLOR": "000000",
        "INV_BACKGROUND_COLOR": "AAAAAA",
        "COLLAPSIBLE_FOREGROUND_COLOR": "000000",
        "COLLAPSIBLE_BACKGROUND_COLOR": "EEEEEE",
        "HOVER_FOREGROUND_COLOR": "EEEEEE",
        "HOVER_BACKGROUND_COLOR": "000000",
    }
    HTML_DARK_THEME = {
        "BODY_FOREGROUND_COLOR": "AAAAAA",
        "BODY_BACKGROUND_COLOR": "000000",
        "INV_FOREGROUND_COLOR": "000000",
        "INV_BACKGROUND_COLOR": "AAAAAA",
        "COLLAPSIBLE_FOREGROUND_COLOR": "AAAAAA",
        "COLLAPSIBLE_BACKGROUND_COLOR": "000000",
        "HOVER_FOREGROUND_COLOR": "111111",
        "HOVER_BACKGROUND_COLOR": "999999",
    }

    def __init__(self):
        self.tui = "tui1"
        self.autolaunch_tui = False
        self.colortheme = "light"
        self.colortheme_colors = self.HTML_LIGHT_THEME
        self.autolaunch_html = True


class Cli:
    def __init__(self):
        self.term = Terminal()
        self.default_config = DefaultConfig()
        self.config_parser = configparser.ConfigParser()
        try:
            self.config_parser.read(CONFIGFILE)
        except Exception:
            self.apply_default_config()

    def _clear_terminal(self) -> None:
        if platform.system() == "Windows":
            subprocess.Popen("cls", shell=True).communicate()
        else:
            print("\033c", end="")

    def _enter_to_continue(self) -> None:
        print("\nPress ENTER to continue...")
        with self.term.cbreak():
            while not self.term.inkey(timeout=0.01).lower():
                pass
        self._clear_terminal()

    def _prompt(self) -> str:
        return "==> pytest-tui configuration menu <==\n"

    def menu_items(self) -> dict:
        return {
            "Apply default config settings": self.apply_default_config_plus_enter,
            "Display current config settings": self.display_current_config,
            "Select TUI": self.select_tui,
            "Set TUI autolaunch option": self.set_tui_autolaunch,
            "Select HTML light or dark theme": self.select_html_light_dark,
            "Set HTML autolaunch option": self.set_html_autolaunch,
            "Define custom HTML color theme": self.define_custom_html_theme,
            "Quit": self.quit,
        }

    def read_config_file(self) -> None:
        try:
            self.config_parser.read(CONFIGFILE)
        except Exception:
            self.apply_default_config()
        if not (
            self.config_parser.has_section("TUI")
            and self.config_parser.has_section("HTML")
            and self.config_parser.has_section("HTML_COLOR_THEME")
        ):
            self.apply_default_config()

    def apply_default_config_plus_enter(self) -> None:
        """Wrapper around 'apply_default_config' to allow for Enter prompt afterwards."""
        self.apply_default_config()
        self._enter_to_continue()

    def apply_default_config(self) -> None:
        """Generate default config, store in local config_parser instance, and write it to file."""
        if not self.config_parser.has_section("TUI"):
            self.config_parser.add_section("TUI")
        self.config_parser.set("TUI", "tui", self.default_config.tui)
        self.config_parser.set(
            "TUI", "autolaunch_tui", str(self.default_config.autolaunch_tui)
        )
        if not self.config_parser.has_section("HTML"):
            self.config_parser.add_section("HTML")
        self.config_parser.set("HTML", "colortheme", self.default_config.colortheme)
        self.config_parser.set(
            "HTML", "autolaunch_html", str(self.default_config.autolaunch_html)
        )
        if not self.config_parser.has_section("HTML_COLOR_THEME"):
            self.config_parser.add_section("HTML_COLOR_THEME")
        for key in self.default_config.colortheme_colors:
            self.config_parser.set(
                "HTML_COLOR_THEME", key, self.default_config.colortheme_colors[key]
            )
        self.write_current_config_to_file()

    def display_current_config(self) -> None:
        """Print the current config settings to the terminal."""
        self._clear_terminal()
        for section in self.config_parser.sections():
            print(f"{section}:")
            for option in self.config_parser.options(section):
                print(f"  {option}: {self.config_parser.get(section, option)}")
        self._enter_to_continue()

    def write_current_config_to_file(self) -> None:
        """Write the current config settings to the config file."""
        with open(CONFIGFILE, "w+") as configfile:
            self.config_parser.write(configfile)

    def select_tui(self) -> None:
        self._clear_terminal()
        tui = Input(
            "Enter the TUI you would like to use ['tui1' | 'tui2']: ", strip=True
        ).launch()
        if tui not in ["tui1", "tui2"]:
            self.select_tui()
            return
        if not self.config_parser.has_section("TUI"):
            self.config_parser.add_section("TUI")
        self.config_parser.set("TUI", "tui", tui)
        self.write_current_config_to_file()
        self._enter_to_continue()

    def set_tui_autolaunch(self) -> None:
        self._clear_terminal()
        autolaunch_tui = YesNo(
            "Autolaunch TUI when test session is complete: "
        ).launch()
        if not self.config_parser.has_section("TUI"):
            self.config_parser.add_section("TUI")
        self.config_parser.set("TUI", "autolaunch_tui", str(autolaunch_tui))
        self.write_current_config_to_file()
        self._enter_to_continue()

    def select_html_light_dark(self) -> None:
        self._clear_terminal()
        colortheme = Input(
            "Enter the HTML theme you would like to use ['light' | 'dark']: ",
            strip=True,
        ).launch()
        if colortheme not in ["light", "dark"]:
            self.select_html_light_dark()
            return
        if not self.config_parser.has_section("HTML"):
            self.config_parser.add_section("HTML")
        self.config_parser.set("HTML", "colortheme", colortheme)

        self.colortheme_colors = (
            self.default_config.HTML_LIGHT_THEME
            if colortheme == "light"
            else self.default_config.HTML_DARK_THEME
        )

        for key in self.colortheme_colors:
            self.config_parser.set("HTML_COLOR_THEME", key, self.colortheme_colors[key])

        self.write_current_config_to_file()
        self._enter_to_continue()

    def define_custom_html_theme(self) -> None:
        self._clear_terminal()
        if not self.config_parser.has_section("HTML_COLOR_THEME"):
            self.config_parser.add_section("HTML_COLOR_THEME")

        val = Input(
            "Enter BODY_FOREGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "BODY_FOREGROUND_COLOR", val)
        val = Input(
            "Enter BODY_BACKGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "BODY_BACKGROUND_COLOR", val)
        val = Input(
            "Enter INV_FOREGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "INV_FOREGROUND_COLOR", val)
        val = Input(
            "Enter INV_BACKGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "INV_BACKGROUND_COLOR", val)
        val = Input(
            "Enter COLLAPSIBLE_FOREGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "COLLAPSIBLE_FOREGROUND_COLOR", val)
        val = Input(
            "Enter COLLAPSIBLE_BACKGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "COLLAPSIBLE_BACKGROUND_COLOR", val)
        val = Input(
            "Enter HOVER_FOREGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "HOVER_FOREGROUND_COLOR", val)
        val = Input(
            "Enter HOVER_BACKGROUND_COLOR value in hex (#xxxxx): ", strip=True
        ).launch()
        self.config_parser.set("HTML_COLOR_THEME", "HOVER_BACKGROUND_COLOR", val)

        self.write_current_config_to_file()
        self._enter_to_continue()

    def set_html_autolaunch(self) -> None:
        self._clear_terminal()
        autolaunch_html = YesNo("Auto-launch HTML when generated: ").launch()
        if not self.config_parser.has_section("HTML"):
            self.config_parser.add_section("HTML")
        self.config_parser.set("HTML", "autolaunch_html", str(autolaunch_html))
        self.write_current_config_to_file()
        self._enter_to_continue()

    def quit(self) -> None:
        self._clear_terminal()
        print("Exiting...")
        sys.exit()

    def run(self) -> None:
        self._clear_terminal()
        cli = Bullet(
            # prompt = self._prompt(),
            choices=list(self.menu_items().keys()),
            bullet="==> ",
            word_color=colors.bright(colors.foreground["white"]),
            word_on_switch=colors.bright(colors.foreground["black"]),
            background_color=colors.bright(colors.background["black"]),
            background_on_switch=colors.bright(colors.background["white"]),
        )
        menu_item = cli.launch()
        while True:
            self._clear_terminal()
            self.menu_items()[menu_item]()
            menu_item = cli.launch()


def tui_launch():
    tuicli = Cli()
    tuicli.read_config_file()
    tui1() if tuicli.config_parser.get("TUI", "tui") == "tui1" else tui2()


def tui_config():
    tuicli = Cli()
    tuicli.read_config_file()
    tuicli.run()


if __name__ == "__main__":
    tui_config()
