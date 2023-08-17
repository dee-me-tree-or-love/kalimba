"""Kalimba == {Coli}`ma {M}enu {Ba}r

A simple Menu Bar app to control your colimba status.
"""
import rumps
import subprocess
import logging as l

l.basicConfig()
logger = l.getLogger(__name__)
logger.setLevel(l.DEBUG)


class StatusMenuItem(rumps.MenuItem):
    def __init__(self):
        super(StatusMenuItem, self).__init__("👀 status")


class KalimbaMenuBarApp(rumps.App):
    __colima_running = False

    def __init__(self):
        super(KalimbaMenuBarApp, self).__init__("Kalimba", "🐳")
        self.__status_menu = StatusMenuItem()
        self.menu = [self.__status_menu, "Toggle"]

    @rumps.clicked("Toggle")
    def start(self, _):
        # TODO(tech-debt): make this call not-blocking but thread safe
        cmd = self.__get_colima_trigger_cmd()
        self.__toggle_colima(cmd)

    # TODO(tech-debt): make the timer configurable
    @rumps.timer(10)
    def check_status(self, _):
        try:
            result = subprocess.run(
                ["colima", "status"],
                text=True,
                check=False,
                capture_output=True,
            )
            output = result.stdout or result.stderr
            logger.debug(output.splitlines())
            status_title = output.splitlines()[0]
            colima_running = "colima is running" in status_title
            status_icon = "🏃" if colima_running else "😴"
            self.__update_status_menu_title(status_title, status_icon)
            self.__update_colima_run_status(colima_running)
        except Exception as error:
            logger.error(error)
            self.__update_status_menu_title("failed to get status...", "🤕")

    def __update_status_menu_title(self, title: str, icon: str):
        self.__status_menu.title = icon + " " + title

    def __update_colima_run_status(self, colima_running: bool):
        self.__colima_running = colima_running

    def __get_colima_trigger_cmd(self) -> str:
        return "stop" if self.__colima_running else "start"

    def __toggle_colima(self, cmd: str):
        try:
            result = subprocess.run(["colima", cmd])
            result.check_returncode()
        except Exception as error:
            logger.error(error)
            rumps.alert("failed to toggle colima...", "🤕")


def run_kalimba():
    KalimbaMenuBarApp().run()


if __name__ == "__main__":
    run_kalimba()
