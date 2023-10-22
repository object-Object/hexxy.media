import logging
import os
from dataclasses import dataclass

import cdktf
from cdktf_cdktf_provider_cloudflare import provider, record
from constructs import Construct

OBJECTOBJECT_CA = "155.138.139.1"
HEXXYCRAFT_PROD = "23.139.82.245"
HEXXYCRAFT_DEV = "131.186.1.24"


@dataclass
class GitHubPagesRecord:
    name: str
    value: str


class HexxyMediaTerraformStack(cdktf.TerraformStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        zone_id: str,
        github_pages: list[GitHubPagesRecord],
    ):
        logging.getLogger(__name__).info(f"Initializing stack: {id}")
        super().__init__(scope, id)

        cdktf.CloudBackend(
            self,
            organization="object-Object",
            workspaces=cdktf.NamedCloudWorkspace("hexxy-media"),
        )

        provider.CloudflareProvider(
            self,
            "CloudflareProvider",
            api_token=os.getenv("CLOUDFLARE_API_TOKEN"),
        )

        for record_type, name, value, proxied in [
            ("A", "*", OBJECTOBJECT_CA, True),
            ("A", "hexxy.media", OBJECTOBJECT_CA, True),
            ("A", "play", HEXXYCRAFT_PROD, False),
            ("A", "dev.play", HEXXYCRAFT_DEV, False),
        ]:
            record.Record(
                self,
                f"{record_type}_{name}_{value}",
                zone_id=zone_id,
                type=record_type,
                name=name,
                value=value,
                proxied=proxied,
            )

        for page in github_pages:
            record.Record(
                self,
                f"GitHubPages_{page.name}_{page.value}",
                zone_id=zone_id,
                type="CNAME",
                name=page.name,
                value=page.value,
            )
