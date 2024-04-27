#!/usr/bin/env python
import logging

import cdktf
from constructs import Construct

from hexxy_media.common.logging import setup_logging

from .stack import GitHubPagesRecord, HexxyMediaTerraformStack

GITHUB_PAGES_RECORDS = [
    GitHubPagesRecord("hexdoc", github_user="hexdoc-dev"),
    GitHubPagesRecord("addons", github_user="samsthenerd"),
    # mod books
    GitHubPagesRecord("book", github_user="hexdoc-dev"),
    GitHubPagesRecord("hexcasting", github_user="fallingcolors"),
    GitHubPagesRecord("hexgloop", github_user="samsthenerd"),
    GitHubPagesRecord("oneironaut", github_user="beholderface"),
    GitHubPagesRecord("hexdebug", github_user="object-Object"),
]


def init_stacks(app: Construct):
    HexxyMediaTerraformStack(
        app,
        "prod",
        organization="object-Object",
        workspace="hexxy-media",
        zone_id="555d45bbbd42d4e084994b80948da2fe",
        github_pages=GITHUB_PAGES_RECORDS,
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Creating app.")
    app = cdktf.App()

    logger.info("Creating stacks.")
    init_stacks(app)

    logger.info("Synthesizing app.")
    app.synth()

    print()


if __name__ == "__main__":
    main()
