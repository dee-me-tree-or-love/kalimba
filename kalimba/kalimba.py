"""Kalimba == {Coli}`ma {M}enu {Ba}r

A simple Menu Bar app to control your colimba status.
"""
import rumps
import subprocess
import logging as l
from concurrent.futures import ThreadPoolExecutor

l.basicConfig()
logger = l.getLogger(__name__)


class StatusMenuItem(rumps.MenuItem):
    def __init__(self):
        super(StatusMenuItem, self).__init__("👀 status")


class ToggleMenuItem(rumps.MenuItem):
    DEFAULT_TITLE = "Toggle"

    def __init__(self):
        super(ToggleMenuItem, self).__init__(self.DEFAULT_TITLE)

    def set_starting(self) -> None:
        self.title = "Starting ..."

    def set_stopping(self) -> None:
        self.title = "Stopping ..."

    def reset(self) -> None:
        self.title = self.DEFAULT_TITLE


class KalimbaMenuBarApp(rumps.App):
    __colima_running = False

    @staticmethod
    def prepare_cli_pool() -> ThreadPoolExecutor:
        return ThreadPoolExecutor(max_workers=1)

    def __init__(self, colima_cli_pool: ThreadPoolExecutor):
        super(KalimbaMenuBarApp, self).__init__("Kalimba", "🐳")
        self.__status_menu = StatusMenuItem()
        self.__toggle_menu = ToggleMenuItem()
        self.menu = [self.__status_menu, self.__toggle_menu]
        self.__colima_cli_single_pool = colima_cli_pool

    @rumps.timer(30)
    def check_status(self, _) -> None:
        self.__check_status_handler()

    def __check_status_handler(self) -> None:
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
            self.__handle_error(error)

    @rumps.clicked(ToggleMenuItem.DEFAULT_TITLE)
    def queued_toggle(self, _) -> None:
        self.__colima_cli_single_pool.submit(self.__toggle_handler)

    def __toggle_handler(self) -> None:
        try:
            if self.__colima_running:
                self.__toggle_menu.set_stopping()
                self.__toggle_colima("stop")
                self.__update_colima_run_status(False)
            else:
                self.__toggle_menu.set_starting()
                self.__toggle_colima("start")
                self.__update_colima_run_status(True)
        except Exception as error:
            self.__handle_error(error)
        finally:
            self.__toggle_menu.reset()

    def __toggle_colima(self, cmd: str) -> None:
        try:
            result = subprocess.run(["colima", cmd])
            result.check_returncode()
        except Exception as error:
            logger.error(error)
            rumps.alert("failed to toggle colima...", "🤕")

    def __update_status_menu_title(self, title: str, icon: str) -> None:
        self.__status_menu.title = icon + " " + title

    def __update_colima_run_status(self, colima_running: bool) -> None:
        self.__colima_running = colima_running

    def __handle_error(self, error: Exception) -> None:
        logger.error(error)
        self.__update_status_menu_title("failed to get status...", "🤕")
        self.__update_colima_run_status(False)


# mem(docs-link): update README if this changes.
def run_kalimba(verbose=False):
    logger.setLevel(l.DEBUG if verbose else l.INFO)
    logger.info("Starting the kalimba app... 🎶")

    with KalimbaMenuBarApp.prepare_cli_pool() as pool:
        KalimbaMenuBarApp(pool).run()


if __name__ == "__main__":
    run_kalimba(verbose=True)
