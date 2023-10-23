#!/usr/bin/env python
import logging

import cdktf
from constructs import Construct

from hexxy_media.common.logging import setup_logging

from .stack import GitHubPagesRecord, HexxyMediaTerraformStack


def init_stacks(app: Construct):
    HexxyMediaTerraformStack(
        app,
        "prod",
        organization="object-Object",
        workspace="hexxy-media",
        zone_id="555d45bbbd42d4e084994b80948da2fe",
        github_pages=[
            GitHubPagesRecord("addons", "samsthenerd.github.io"),
            GitHubPagesRecord("hexgloop", "samsthenerd.github.io"),
            GitHubPagesRecord("hexal-dev", "object-object.github.io"),
        ],
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
