"""Kalimba == {Coli}`ma {M}enu {Ba}r

A simple Menu Bar app to control your colimba status.
"""
import rumps
import subprocess
import logging as l
from concurrent.futures import ThreadPoolExecutor

l.basicConfig()
logger = l.getLogger(__name__)


class KalimbaIcons:
    WHALE = "🐳"
    LOOKING = "👀"
    SLEEP = "🐚"
    RUN = "🐠"
    BROKEN = "🙊"
    TUNE = "🎶"


class KalimbaMessages:
    APP_TITLE = "Kalimba"
    APP_STARTING = f"Starting the kalimba app... {KalimbaIcons.TUNE}"
    COLIMA_RUNNING = "colima is running"
    COLIMA_STARTING = "Starting ..."
    COLIMA_STOPPING = "Stopping ..."
    FAILED_TOGGLE = "failed to toggle colima..."
    FAILED_STATUS = "failed to get status..."


class KalimbaThreadPoolExecutor(ThreadPoolExecutor):
    pass


class StatusMenuItem(rumps.MenuItem):
    def __init__(self):
        super(StatusMenuItem, self).__init__(f"${KalimbaIcons.LOOKING} status")


class ToggleMenuItem(rumps.MenuItem):
    DEFAULT_TITLE = "Toggle"

    def __init__(self):
        super(ToggleMenuItem, self).__init__(self.DEFAULT_TITLE)

    def set_starting(self) -> None:
        self.title = KalimbaMessages.COLIMA_STARTING

    def set_stopping(self) -> None:
        self.title = KalimbaMessages.COLIMA_STOPPING

    def reset(self) -> None:
        self.title = self.DEFAULT_TITLE


class ColimaCli:
    __cli__ = "colima"

    @classmethod
    def get_status(cls) -> tuple:
        opts = dict(text=True, check=False, capture_output=True)
        result = subprocess.run([cls.__cli__, "status"], **opts)
        output = result.stdout or result.stderr
        output_lines = output.splitlines()
        logger.debug(output_lines)
        status_title = output_lines[0]
        return status_title, output_lines[1:]

    @classmethod
    def start_engine(cls) -> bool:
        cls.__toggle_engine("start")

    @classmethod
    def stop_engine(cls) -> bool:
        cls.__toggle_engine("stop")

    @classmethod
    def __toggle_engine(cls, cmd: str) -> None:
        result = subprocess.run([cls.__cli__, cmd])
        result.check_returncode()


class KalimbaMenuBarApp(rumps.App):
    __colima_running = False
    __colima_cli = ColimaCli

    @staticmethod
    def prepare_cli_pool() -> KalimbaThreadPoolExecutor:
        return KalimbaThreadPoolExecutor(max_workers=1)

    def __init__(self, colima_cli_pool: KalimbaThreadPoolExecutor):
        super(KalimbaMenuBarApp, self).__init__(
            KalimbaMessages.APP_TITLE, KalimbaIcons.WHALE
        )
        self.__colima_cli_single_pool = colima_cli_pool
        self.__status_menu = StatusMenuItem()
        self.__toggle_menu = ToggleMenuItem()
        self.menu = [self.__status_menu, self.__toggle_menu]

    @rumps.timer(30)
    def check_status(self, _) -> None:
        self.__check_status_handler()

    def __check_status_handler(self) -> None:
        try:
            status_title, _ = self.__colima_cli.get_status()
            colima_running = KalimbaMessages.COLIMA_RUNNING in status_title
            status_icon = KalimbaIcons.RUN if colima_running else KalimbaIcons.SLEEP
            self.__update_status_menu_title(status_title, status_icon)
            self.__update_colima_run_status(colima_running)
        except Exception as error:
            logger.error(error)
            alert_args = (KalimbaMessages.FAILED_STATUS, KalimbaIcons.BROKEN)
            self.__update_status_menu_title(*alert_args)
            self.__update_colima_run_status(False)

    @rumps.clicked(ToggleMenuItem.DEFAULT_TITLE)
    def queued_toggle(self, _) -> None:
        self.__colima_cli_single_pool.submit(self.__toggle_handler)

    def __toggle_handler(self) -> None:
        try:
            if self.__colima_running:
                self.__toggle_menu.set_stopping()
                self.__colima_cli.stop_engine()
                self.__update_colima_run_status(False)
            else:
                self.__toggle_menu.set_starting()
                self.__colima_cli.start_engine()
                self.__update_colima_run_status(True)
        except Exception as error:
            logger.error(error)
            alert_args = (KalimbaMessages.FAILED_TOGGLE, KalimbaIcons.BROKEN)
            rumps.alert(*alert_args)
            self.__update_status_menu_title(*alert_args)
        finally:
            self.__toggle_menu.reset()

    def __update_status_menu_title(self, title: str, icon: str) -> None:
        self.__status_menu.title = icon + " " + title

    def __update_colima_run_status(self, colima_running: bool) -> None:
        self.__colima_running = colima_running


# mem(docs-link): update README if this changes.
def run_kalimba(verbose=False):
    logger.setLevel(l.DEBUG if verbose else l.INFO)
    logger.info(KalimbaMessages.APP_STARTING)

    with KalimbaMenuBarApp.prepare_cli_pool() as pool:
        KalimbaMenuBarApp(pool).run()


if __name__ == "__main__":
    run_kalimba(verbose=True)
