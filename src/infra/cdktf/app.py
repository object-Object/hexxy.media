#!/usr/bin/env python
import logging

import cdktf
from constructs import Construct

from hexxy_media.common.logging import setup_logging

from .stack import GitHubPagesRecord, HexxyMediaTerraformStack, IPWithPort


def init_stacks(app: Construct):
    HexxyMediaTerraformStack(
        app,
        "prod",
        organization="object-Object",
        workspace="hexxy-media",
        zone_id="555d45bbbd42d4e084994b80948da2fe",
        github_pages=[
            GitHubPagesRecord("hexdoc", github_user="hexdoc-dev"),
            GitHubPagesRecord("addons", github_user="samsthenerd"),
            # mod books
            GitHubPagesRecord("book", github_user="hexdoc-dev"),
            GitHubPagesRecord("hexcasting", github_user="fallingcolors"),
            GitHubPagesRecord("hexgloop", github_user="samsthenerd"),
            GitHubPagesRecord("oneironaut", github_user="beholderface"),
            GitHubPagesRecord("ephemera", github_user="beholderface"),
            GitHubPagesRecord("hexdebug", github_user="object-object"),
            GitHubPagesRecord("hexbound", github_user="object-object"),
        ],
        objectobject_ca="155.138.139.1",
        hexxytest="172.92.208.70",
        cypher_mc=IPWithPort("185.137.94.42", 25591),
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
