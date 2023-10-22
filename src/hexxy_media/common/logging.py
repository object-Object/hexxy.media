import logging


def setup_logging(verbose: bool = False):
    if verbose:
        level = logging.DEBUG
        fmt = "[ {asctime} | {name} | {levelname} ]  {message}"
    else:
        level = logging.INFO
        fmt = "[ {asctime} | {levelname} ]  {message}"

    logging.basicConfig(
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        format=fmt,
        level=level,
    )
    logging.getLogger(__name__).debug("Logger initialized.")
