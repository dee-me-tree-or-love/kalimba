import click
import logging as l
from kalimba.kalimba import run_kalimba


l.basicConfig()
logger = l.getLogger(__name__)

APP_NAME = "kalimba"


def __run_detached_kalimba(*_):
    logger.debug(f"starting {APP_NAME} in detached mode")
    raise NotImplementedError(
        "Sorry... this is not yet implemented. "
        + f"Please run {APP_NAME} as a shell background process with `&` for now."
    )


def __run_foreground_kalimba(verbose: bool):
    logger.debug(f"starting {APP_NAME} in foreground mode")
    run_kalimba(verbose=verbose)


@click.command()
@click.option(
    "-d",
    "--detached",
    is_flag=True,
    default=False,
    help=f"Run the {APP_NAME} process in a detached (sub-process) mode",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help=f"Run the {APP_NAME} process with extended logging",
)
def start(detached: bool, verbose: bool):
    # TODO(tech-debt): make sure Kalimba here is also taken from the APP_NAME variable.
    """Simple starter for Kalimba (Colima Menu Bar) app"""
    logger.setLevel(l.DEBUG if verbose else l.INFO)
    runner = __run_detached_kalimba if detached else __run_foreground_kalimba
    runner(verbose)


if __name__ == "__main__":
    start()
