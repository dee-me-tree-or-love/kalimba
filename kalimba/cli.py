import click
import logging as l
from kalimba.kalimba import run_kalimba


l.basicConfig()
logger = l.getLogger(__name__)
logger.setLevel(l.INFO)

APP_NAME = "kalimba"


def __run_detached_kalimba(*_):
    l.info(f"starting {APP_NAME} in detached mode")
    raise NotImplementedError("Sorry... this is not yet implemented")


def __run_foreground_kalimba(verbose: bool):
    l.info(f"starting {APP_NAME} in foreground mode")
    run_kalimba(verbose=verbose)


@click.command()
@click.option(
    "--detached/--foreground",
    default=False,
    help="Run the Kalimba process in a detached (sub-process) or foreground mode",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Run the Kalimba process with extended logging",
)
def start(detached: bool, verbose: bool):
    """Simple starter for Kalimba"""
    if detached:
        __run_detached_kalimba(verbose)
    else:
        __run_foreground_kalimba(verbose)


if __name__ == "__main__":
    start()
