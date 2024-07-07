import logging

_is_setup = False


def setup_logging(verbose: bool = False):
    global _is_setup
    if _is_setup:
        return
    _is_setup = True

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
