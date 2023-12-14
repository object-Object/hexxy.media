import logging
import os
from dataclasses import dataclass

import cdktf
from cdktf_cdktf_provider_cloudflare import provider, record
from constructs import Construct

OBJECTOBJECT_CA = "155.138.139.1"


@dataclass
class GitHubPagesRecord:
    subdomain: str
    github_user: str

    @property
    def url(self):
        return f"https://{self.subdomain}.hexxy.media"

    @property
    def value(self):
        return f"{self.github_user}.github.io"


class HexxyMediaTerraformStack(cdktf.TerraformStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        organization: str,
        workspace: str,
        zone_id: str,
        github_pages: list[GitHubPagesRecord],
    ):
        logging.getLogger(__name__).info(f"Initializing stack: {id}")
        super().__init__(scope, id)

        cdktf.CloudBackend(
            self,
            organization=organization,
            workspaces=cdktf.NamedCloudWorkspace(workspace),
        )

        provider.CloudflareProvider(
            self,
            "CloudflareProvider",
            api_token=os.getenv("CLOUDFLARE_API_TOKEN"),
        )

        for record_type, name, value, proxied in [
            ("A", "*", OBJECTOBJECT_CA, True),
            ("A", "hexxy.media", OBJECTOBJECT_CA, True),
            # ("A", "play", HEXXYCRAFT_PROD, False),
            # ("A", "dev.play", HEXXYCRAFT_DEV, False),
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
                f"GitHubPages_{page.subdomain}_{page.value}",
                zone_id=zone_id,
                type="CNAME",
                name=page.subdomain,
                value=page.value,
            )
