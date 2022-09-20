# import configparser
# import platform
# import subprocess
# import sys

# from blessed import Terminal
# from bullet import Bullet, Input, YesNo, colors
# from rich import print

# from pytest_tui.tui import main as tui
# from pytest_tui.utils import CONFIGFILE


# class DefaultConfig:
#     def __init__(self):
#         self.tui_autolaunch = False
#         self.html_autolaunch = False


# class Cli:
#     def __init__(self):
#         self.term = Terminal()
#         self.default_config = DefaultConfig()
#         self.config_parser = configparser.ConfigParser()
#         try:
#             self.config_parser.read(CONFIGFILE)
#         except Exception:
#             self.apply_default_config()

#     def _clear_terminal(self) -> None:
#         if platform.system() == "Windows":
#             subprocess.Popen("cls", shell=True).communicate()
#         else:
#             print("\033c", end="")

#     def _enter_to_continue(self) -> None:
#         print("\nPress ENTER to continue...")
#         with self.term.cbreak():
#             while not self.term.inkey(timeout=0.01).lower():
#                 pass
#         self._clear_terminal()

#     def _prompt(self) -> str:
#         return "==> pytest-tui configuration menu <==\n"

#     def menu_items(self) -> dict:
#         return {
#             "Display current config settings": self.display_current_config,
#             "Apply default config settings": self.apply_default_config_plus_enter,
#             "Set TUI autolaunch option": self.set_tui_autolaunch,
#             "Set HTML autolaunch option": self.set_html_autolaunch,
#             "Quit": self.quit,
#         }

#     def read_config_file(self) -> None:
#         try:
#             self.config_parser.read(CONFIGFILE)
#         except Exception:
#             self.apply_default_config()
#         if not (
#             self.config_parser.has_section("TUI")
#             and self.config_parser.has_section("HTML")
#         ):
#             self.apply_default_config()
#         self.tui_autolaunch = self.config_parser.getboolean("TUI", "tui_autolaunch")
#         self.html_autolaunch = self.config_parser.getboolean("HTML", "html_autolaunch")

#     def apply_default_config_plus_enter(self) -> None:
#         """Wrapper around 'apply_default_config' to allow for Enter prompt afterwards."""
#         self.apply_default_config()
#         self._enter_to_continue()

#     def apply_default_config(self) -> None:
#         """Generate default config, store in local config_parser instance, and write it to file."""
#         if not self.config_parser.has_section("TUI"):
#             self.config_parser.add_section("TUI")
#         self.config_parser.set(
#             "TUI", "tui_autolaunch", str(self.default_config.tui_autolaunch)
#         )
#         if not self.config_parser.has_section("HTML"):
#             self.config_parser.add_section("HTML")
#         self.config_parser.set(
#             "HTML", "html_autolaunch", str(self.default_config.html_autolaunch)
#         )
#         self.write_current_config_to_file()

#     def display_current_config(self) -> None:
#         """Print the current config settings to the terminal."""
#         self._clear_terminal()
#         for section in self.config_parser.sections():
#             print(f"{section}:")
#             for option in self.config_parser.options(section):
#                 print(f"  {option}: {self.config_parser.get(section, option)}")
#         self._enter_to_continue()

#     def write_current_config_to_file(self) -> None:
#         """Write the current config settings to the config file."""
#         with open(CONFIGFILE, "w+") as configfile:
#             self.config_parser.write(configfile)

#     def set_tui_autolaunch(self) -> None:
#         self._clear_terminal()
#         tui_autolaunch = YesNo(
#             "Autolaunch TUI when test session is complete: "
#         ).launch()
#         if not self.config_parser.has_section("TUI"):
#             self.config_parser.add_section("TUI")
#         self.config_parser.set("TUI", "tui_autolaunch", str(tui_autolaunch))
#         self.write_current_config_to_file()
#         self._enter_to_continue()

#     def set_html_autolaunch(self) -> None:
#         self._clear_terminal()
#         html_autolaunch = YesNo("Auto-launch HTML when generated: ").launch()
#         if not self.config_parser.has_section("HTML"):
#             self.config_parser.add_section("HTML")
#         self.config_parser.set("HTML", "html_autolaunch", str(html_autolaunch))
#         self.write_current_config_to_file()
#         self._enter_to_continue()

#     def quit(self) -> None:
#         self._clear_terminal()
#         print("Exiting...")
#         sys.exit()

#     def run(self) -> None:
#         self._clear_terminal()
#         self.cli = Bullet(
#             # prompt = self._prompt(),
#             choices=list(self.menu_items().keys()),
#             bullet="==> ",
#             word_color=colors.bright(colors.foreground["white"]),
#             word_on_switch=colors.bright(colors.foreground["black"]),
#             background_color=colors.bright(colors.background["black"]),
#             background_on_switch=colors.bright(colors.background["white"]),
#         )
#         self.menu_item = self.cli.launch()
#         while True:
#             self._clear_terminal()
#             self.menu_items()[self.menu_item]()
#             self.menu_item = self.cli.launch()


# def tui_run():
#     tui()


# def tui_launch():
#     tuicli = Cli()
#     tuicli.read_config_file()
#     if tuicli.config_parser["TUI"].get("tui_autolaunch") == "True":
#         tui()


# def tui_config():
#     tuicli = Cli()
#     tuicli.read_config_file()
#     tuicli.run()


# if __name__ == "__main__":
#     tui_config()
