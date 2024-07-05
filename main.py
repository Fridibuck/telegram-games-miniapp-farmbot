import imgui
from imgui.integrations.pyglet import create_renderer
import pyglet
import time
import threading
import re
import webbrowser
from tkinter import Tk, filedialog
import subprocess
from pyglet.gl import glClearColor
from colorama import init, Fore, Style
import sys
import io
import os

# Check if sys.stdout is not None before wrapping it
if sys.stdout:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

init(autoreset=True)

class RayTeakMenu:
    def __init__(self):
        self.scripts = {
            "Blum": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Hamsterkombat": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Yescoin": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Timefarm": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Pixelverse": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Dotcoin": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "MatchQuest": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Spinnercoin": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
            "Dejendog": {"status": False, "filepath": "", "loaded": False, "log": "", "process": None, "show_log": False},
        }

        self.links = {
            "Blum": "t.me/BlumCryptoBot/app?startapp=ref_h6dmca5EQu",
            "Hamsterkombat": "https://t.me/hamster_kombat_Bot/start?startapp=kentId1202532315",
            "Yescoin": "https://t.me/theYescoin_bot/Yescoin?startapp=c7g96d",
            "Timefarm": "https://t.me/TimeFarmCryptoBot?start=1z3HV3nGOoVPegEs2",
            "Pixelverse": "https://t.me/pixelversexyzbot?start=1202532315",
            "Dotcoin": "https://t.me/dotcoin_bot?start=1202532315",
            "MatchQuest": "https://t.me/matchquest_bot?start=1202532315",
            "Spinnercoin": "https://t.me/spinnercoin_bot?start=1202532315",
            "Dejendog": "https://t.me/dejendog_bot?start=1202532315",
        }

        self.open_tabs = {}

    def show(self):
        imgui.set_next_window_size(300, 600)
        imgui.set_next_window_position(0, 0)

        imgui.begin("Telegram mini games bot v.1", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)

        if imgui.begin_tab_bar("Scripts"):
            if imgui.begin_tab_item("Manage Scripts")[0]:
                self.show_script_management()
                imgui.end_tab_item()

            for tab_name in self.open_tabs:
                if imgui.begin_tab_item(tab_name)[0]:
                    self.show_log_window(tab_name)
                    imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end()

        # Sağ alt köşeye yazıyı yerleştirmek
        window_width, window_height = imgui.get_io().display_size.x, imgui.get_io().display_size.y
        self.show_footer(window_width, window_height)


    def load_script(self, script_data, script_name):
        Tk().withdraw()
        initialdir = "path/to/your/scripts"  # Set this to the directory where your scripts are located
        filepath = filedialog.askopenfilename(
            initialdir=initialdir,
            filetypes=[("Python Files", f"{script_name.lower()}*.py")]
        )
        if filepath:
            script_data["filepath"] = filepath
            script_data["loaded"] = True


    def show_script_management(self):
        for script_name, script_data in self.scripts.items():
            expanded, visible = imgui.collapsing_header(script_name)
            if expanded:
                filename = script_data["filepath"].split("/")[-1] if script_data["filepath"] else ""
                changed, filename = imgui.input_text("Script File##" + script_name, filename, 256, imgui.INPUT_TEXT_READ_ONLY)
                if imgui.button("Load##" + script_name):
                    self.load_script(script_data, script_name)
                imgui.same_line()
                if imgui.button("Unload##" + script_name):
                    self.stop_script(script_data)
                    script_data["loaded"] = False
                    script_data["filepath"] = ""  # Seçili dosya adını temizle

                if script_data["loaded"]:
                    if imgui.button("Start##" + script_name):
                        self.start_script(script_name, script_data)
                    imgui.same_line()
                    if imgui.button("Stop##" + script_name):
                        self.stop_script(script_data)

                imgui.text("Status: ")
                imgui.same_line()
                if script_data["status"]:
                    imgui.text_colored("ON", 0, 1, 0, 1)
                else:
                    imgui.text_colored("OFF", 1, 0, 0, 1)

                if imgui.button("Show Log##" + script_name):
                    self.open_tabs[script_name] = script_data

                imgui.same_line()
                if imgui.button("Link##" + script_name):
                    if script_name in self.links:
                        webbrowser.open_new_tab(self.links[script_name])

        imgui.text("Framerate: ")
        imgui.same_line()
        imgui.text_colored("%.1f FPS" % imgui.get_io().framerate, 0.0, 1.0, 0.0, 1.0)

        imgui.text("Server Status: ")
        imgui.same_line()
        if any(script["status"] for script in self.scripts.values()):
            imgui.text_colored("ON", 0, 1, 0, 1)
        else:
            imgui.text_colored("OFF", 1, 0, 0, 1)

        running_scripts = sum(script["status"] for script in self.scripts.values())
        imgui.text(f"Running Scripts: {running_scripts}") 



    def start_script(self, script_name, script_data):
        if script_data["filepath"] and not script_data["status"]:
            # Create the startupinfo object to prevent the terminal window from opening
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            script_data["process"] = subprocess.Popen(
                ['python', script_data["filepath"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=startupinfo
            )
            script_data["status"] = True
            script_data["log"] = ""
            threading.Thread(target=self.read_output, args=(script_name, script_data), daemon=True).start()

    def stop_script(self, script_data):
        if script_data.get("process"):
            script_data["process"].terminate()
            script_data["process"].wait()
            script_data["status"] = False


    def read_output(self, script_name, script_data):
        while script_data["status"]:
            output = script_data["process"].stdout.readline()
            if output:
                # Add color based on some conditions
                if "Balance" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Farming" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Getting token" in output or "Token obtained" in output:
                    output = Fore.BLUE + output + Style.RESET_ALL
                elif "Ref Balance" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Game" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Task" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Tap" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Info" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Box" in output:
                    output = Fore.BLUE + output + Style.RESET_ALL
                elif "Pet" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Upgrade" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Error" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Success" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Fail" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Fetching" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Submitting" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Claiming" in output:
                    output = Fore.BLUE + output + Style.RESET_ALL
                elif "Starting" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Finishing" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Checking" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Level" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Logging in" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "===== [ " in output:  # For user headers
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "[ Telegram ID ]:" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "availableAmount" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "[ Tap ]:" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Remaining" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Reprocessing all accounts" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Error getting task list" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Level up failed" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Login failed" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Upgrading" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Claim time" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Claimed" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Checking ticket" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Ticket" in output:
                    output = Fore.BLUE + output + Style.RESET_ALL
                elif "Total earned" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Coin" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Energy" in output:
                    output = Fore.BLUE + output + Style.RESET_ALL
                elif "Exchange" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Passive earnings" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Booster" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Daily reward" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Account" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Squad" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Collecting" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Recovery" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Energy limit" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Bar Amount" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Gold Amount" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Missing" in output:
                    output = Fore.RED + output + Style.RESET_ALL
                elif "Buy Pet" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Waiting for the next request" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Dotcoin BOT" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Processing all accounts" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "token successfully created" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Blum BOT" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Complete" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Hamster Kombat BOT!" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Obtaining tokens..." in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Token successfully obtained" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Retrieving user information" in output:
                    output = Fore.CYAN + output + Style.RESET_ALL
                elif "Total Earned" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                elif "Passive Earning" in output:
                    output = Fore.MAGENTA + output + Style.RESET_ALL
                elif "Daily Login" in output:
                    output = Fore.YELLOW + output + Style.RESET_ALL
                elif "Yescoin BOT!" in output:
                    output = Fore.GREEN + output + Style.RESET_ALL
                script_data["log"] += output
            else:
                break

    def show_log_window(self, script_name):
        script_data = self.open_tabs[script_name]
        imgui.set_next_window_size(220, 400)
        imgui.text("Log output:")
        imgui.separator()
        self.display_log(script_data["log"])

    def display_log(self, log):
        lines = log.split('\n')
        for line in lines:
            parts = self.parse_ansi_color(line)
            for color, text in parts:
                imgui.text_colored(text, *color)

    def parse_ansi_color(self, text):
        ansi_color_map = {
            '30': (0.0, 0.0, 0.0, 1.0),  # Black
            '31': (1.0, 0.0, 0.0, 1.0),  # Red
            '32': (0.0, 1.0, 0.0, 1.0),  # Green
            '33': (1.0, 1.0, 0.0, 1.0),  # Yellow
            '34': (0.0, 0.0, 1.0, 1.0),  # Blue
            '35': (1.0, 0.0, 1.0, 1.0),  # Magenta
            '36': (0.0, 1.0, 1.0, 1.0),  # Cyan
            '37': (1.0, 1.0, 1.0, 1.0),  # White
            '90': (0.5, 0.5, 0.5, 1.0),  # Bright Black (Gray)
            '91': (1.0, 0.5, 0.5, 1.0),  # Bright Red
            '92': (0.5, 1.0, 0.5, 1.0),  # Bright Green
            '93': (1.0, 1.0, 0.5, 1.0),  # Bright Yellow
            '94': (0.5, 0.5, 1.0, 1.0),  # Bright Blue
            '95': (1.0, 0.5, 1.0, 1.0),  # Bright Magenta
            '96': (0.5, 1.0, 1.0, 1.0),  # Bright Cyan
            '97': (1.0, 1.0, 1.0, 1.0)   # Bright White
        }

        parts = re.split(r'(\x1b\[[0-9;]*m)', text)
        color = (1.0, 1.0, 1.0, 1.0)  # Default white color
        result = []
        for part in parts:
            if re.match(r'\x1b\[[0-9;]*m', part):
                codes = part[2:-1].split(';')
                for code in codes:
                    if code in ansi_color_map:
                        color = ansi_color_map[code]
            else:
                if part:
                    result.append((color, part))
        return result

    def show_footer(self, window_width, window_height):
        # Sağ alt köşeye yazıyı yerleştirmek ve daha belirgin yapmak
        imgui.set_next_window_position(window_width - 155, window_height - 30)
        
        # Begin a child window with transparent background
        imgui.begin("Footer", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BACKGROUND)
        
        # Add more visible text with mixed colors
        imgui.text_colored("created by", 1.0, 1.0, 1.0, 1.0)  # Beyaz renk
        imgui.same_line()
        imgui.text_colored("@forNINE", 1.0, 0.0, 0.0, 1.0)  # Kırmızı renk
        
        # End the window
        imgui.end()


class SplashScreen:
    def __init__(self):
        self.start_time = time.time()
        self.animation = pyglet.image.load_animation('load.gif')
        self.sprite = pyglet.sprite.Sprite(self.animation)

    def show(self, window):
        elapsed_time = time.time() - self.start_time
        window_width, window_height = window.width, window.height
        self.sprite.x = (window_width - self.sprite.width) // 2
        self.sprite.y = (window_height - self.sprite.height) // 2
        self.sprite.draw()

        return elapsed_time >= 3  # Show for approximately 3 seconds

def main():
    pid = os.getpid()
    user = os.getlogin()
    window_title = f"[{user} {pid}] Mini App"

    window = pyglet.window.Window(width=300, height=600, caption=window_title, resizable=False)
    glClearColor(0, 0, 0, 1)
    imgui.create_context()
    impl = create_renderer(window)

    menu = RayTeakMenu()
    splash_screen = SplashScreen()
    splash_complete = False

    @window.event
    def on_draw():
        nonlocal splash_complete
        window.clear()
        imgui.new_frame()

        if not splash_complete:
            splash_complete = splash_screen.show(window)
        else:
            menu.show()

        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.app.run()
    impl.shutdown()

if __name__ == "__main__":
    main()