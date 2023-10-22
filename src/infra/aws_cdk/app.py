import logging

import aws_cdk as cdk
from constructs import Construct

from hexxy_media.common.logging import setup_logging

from .stack import HexxyMediaCDKStack


def init_stacks(app: Construct):
    HexxyMediaCDKStack(
        app,
        deployment_stage="prod",
        env=cdk.Environment(
            account="511603859520",
            region="us-east-1",
        ),
        artifacts_bucket_name="prod-objectobject-ca-codedeploy-artifacts",
        on_premise_instance_tag="prod-objectobject-ca",
        oidc_owner="object-Object",
        oidc_repo="hexxy.media",
        oidc_environment="prod-codedeploy",
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Creating app.")
    app = cdk.App()

    logger.info("Creating stacks.")
    init_stacks(app)

    logger.info("Synthesizing app.")
    app.synth()

    print()


if __name__ == "__main__":
    main()
