# pyright: reportUnknownMemberType=none

import logging
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socket import socket
from typing import Annotated, Any, cast

import importlib_resources
from typer import Option, Typer
from typing_extensions import override

from hexxy_media.common.logging import setup_logging

from .jinja import build_jinja
from .sitemap import build_sitemap

logger = logging.getLogger(__name__)

app = Typer()


@app.command()
def build(
    *,
    output_dir: Annotated[Path, Option("--out", "-o")] = Path("_site"),
    clean: bool = True,
    hot_reload: bool = False,
    verbose: Annotated[bool, Option("--verbose", "-v")] = False,
):
    setup_logging(verbose)

    # prepare build dir

    build_dir = Path("build/_site")

    if build_dir.exists():
        logger.debug(f"Removing existing files in {build_dir}.")
        shutil.rmtree(build_dir, ignore_errors=True)

    build_dir.mkdir(parents=True, exist_ok=True)

    # build site

    # bypass Jekyll on GitHub Pages
    (build_dir / ".nojekyll").touch()

    logger.info("Copying static files.")
    static_files = importlib_resources.files() / "static"
    with cast(Path, importlib_resources.as_file(static_files)) as static_dir:
        shutil.copytree(static_dir, build_dir, dirs_exist_ok=True)

    build_jinja(build_dir, hot_reload=hot_reload)

    build_sitemap(build_dir)

    # copy from build to output (so we don't wipe the output if a failure occurs)

    logger.info(f"Copying files from {build_dir} to {output_dir}.")

    if clean and output_dir.exists():
        logger.info(f"Removing existing files in {output_dir}.")
        shutil.rmtree(output_dir, ignore_errors=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(build_dir, output_dir, dirs_exist_ok=True)

    logger.info("Done.")


@app.command()
def serve(
    *,
    output_dir: Annotated[Path, Option("--out", "-o")] = Path("_site"),
    port: int = 8000,
    verbose: Annotated[bool, Option("--verbose", "-v")] = False,
):
    setup_logging(verbose)

    logger.info("Building website.")
    build(
        output_dir=output_dir,
        verbose=verbose,
        hot_reload=True,
    )

    class RequestHandler(SimpleHTTPRequestHandler):
        def __init__(
            self,
            request: socket | tuple[bytes, socket],
            client_address: Any,
            server: HTTPServer,
        ) -> None:
            super().__init__(
                request,
                client_address,
                server,
                directory=output_dir.absolute().as_posix(),
            )

        @override
        def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
            if self.command != "HEAD":
                super().log_request(code, size)

    logger.info(f"Serving website at http://localhost:{port} (press ctrl+c to exit).\n")
    with HTTPServer(("", port), RequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            # ignore KeyboardInterrupt to stop Typer from printing "Aborted."
            # because it keeps printing after nodemon exits and breaking the output
            pass


if __name__ == "__main__":
    app()
