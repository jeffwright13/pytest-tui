import configparser
import platform
import subprocess
import sys
from pathlib import Path

from blessed import Terminal
from bullet import Bullet, Input, YesNo, colors
# from rich import print
from single_source import get_version
from pytest_tui.utils import CONFIGFILE
from pytest_tui.tui2 import main as tui2
from pytest_tui.tui1 import main as tui1


class Config:
    TUI_DEFAULT = {
        "tui": "tui1",
        "autolaunch": False,
    }

    HTML_DEFAULT = {
        "autolaunch": False,
        "color_theme": "light",
    }

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
    HTML_DEFAULT_COLORS = HTML_LIGHT_THEME

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIGFILE)
        print(f"{self.config}")


class Cli:
    def __init__(self):
        self.term = Terminal()
        self.config = Config()
        self.tui = "tui1"
        self.tui_auto = "False"
        self.html_auto = "False"
        self.html_theme = "light"

    def _clear_terminal(self):
        if platform.system() == "Windows":
            subprocess.Popen("cls", shell=True).communicate()
        else:
            print("\033c", end="")

    def _enter_to_continue(self):
        print("\nPress ENTER to continue...")
        with self.term.cbreak():
            while not self.term.inkey(timeout=0.01).lower():
                pass
        self._clear_terminal()

    def _prompt(self) -> str:
        return "==> pytest-tui configuration menu <==\n"

    def _menu_items(self) -> dict:
        return {
            "Apply default config settings": self.configure_default,
            "Display config settings": self.show_config,
            "Select TUI ": self.configure_tui,
            "Enable TUI autolaunch": self.configure_tui_auto,
            "Enable HTML autolaunch": self.configure_html_auto,
            "Select HTML light or dark theme": self.configure_html_theme,
            "Quit": self.quit,
        }

    def configure_default(self) -> None:
        self._clear_terminal()
        print(f"Setting config file {CONFIGFILE} to default values...")
        config = configparser.ConfigParser()
        config["TUI"] = self.config.TUI_DEFAULT
        config["HTML"] = self.config.HTML_DEFAULT
        with open(CONFIGFILE, "w+") as configfile:
            config.write(configfile)
        self._enter_to_continue()

    def write_config(self) -> None:
        config = configparser.ConfigParser()
        config["TUI"] = {
            "tui": self.tui,
            "autolaunch": self.tui_auto,
        }
        config["HTML"] = {
            "autolaunch": self.html_auto,
            "color_theme": self.html_theme,
        }
        with open(CONFIGFILE, "w+") as configfile:
            config.write(configfile)

    def configure_tui(self) -> None:
        self._clear_terminal()
        self.tui = Input(
            "Enter the TUI you would like to use ['tui1' | 'tui2']: ", strip=True
        ).launch()
        if self.tui not in ["tui1", "tui2"]:
            self.configure_tui()
            return
        self.write_config()
        # self._enter_to_continue()
        self._clear_terminal()

    def configure_tui_auto(self) -> None:
        self._clear_terminal()
        self.tui_auto = YesNo("Autolaunch the TUI? ").launch()
        self.write_config()
        # self._enter_to_continue()
        self._clear_terminal()

    def configure_html_theme(self) -> None:
        self._clear_terminal()
        self.html_theme = Input(
            "Enter the HTML theme you would like to use ['light' | 'dark']: ", strip=True
        ).launch()
        if self.html_theme not in ["light", "dark"]:
            self.configure_html_theme()
            return
        self.write_config()
        # self._enter_to_continue()
        self._clear_terminal()

    def configure_html_auto(self) -> None:
        self._clear_terminal()
        self.html_auto = YesNo("Autolaunch HTML report? ").launch()
        self.write_config()
        # self._enter_to_continue()
        self._clear_terminal()

    def show_config(self) -> None:
        self._clear_terminal()
        config = configparser.ConfigParser()
        try:
            with open(CONFIGFILE, "r") as configfile:
                config.read_file(configfile)
                for section in config.sections():
                    print(f"{section}:")
                    for key in config[section]:
                        print(f"  {key}: {config[section][key]}")
        except:
            print("No config file found. Setting to default values...")
            self.configure_default()
        finally:
            self._enter_to_continue()


    def quit(self) -> None:
        self._clear_terminal()
        print("Exiting...")
        sys.exit()

    def run(self) -> None:
        self._clear_terminal()
        cli = Bullet(
            # prompt = self._prompt(),
            choices=list(self._menu_items().keys()),
            bullet="==> ",
            word_color=colors.bright(colors.foreground["white"]),
            word_on_switch=colors.bright(colors.foreground["black"]),
            background_color=colors.bright(colors.background["black"]),
            background_on_switch=colors.bright(colors.background["white"]),
        )
        menu_item = cli.launch()
        while True:
            self._clear_terminal()
            self._menu_items()[menu_item]()
            menu_item = cli.launch()
            # self._clear_terminal()

def tui_launch():
    config = Config().config
    print("")

def tui_config():
    tuicli = Cli()
    tuicli.run()

if __name__ == "__main__":
    tui_config()
