import logging
import os
from dataclasses import dataclass
from typing import Any

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
    def name(self):
        return self.subdomain

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

        # simple records
        for record_type, records in {
            "A": {
                "*": (OBJECTOBJECT_CA, True),
                "@": (OBJECTOBJECT_CA, True),
                "hexxytest": ("172.92.208.70", False),
            },
            "TXT": {
                "_visual-studio-marketplace-hexdoc-dev.hexxy.media": (
                    "b5247f90-1e08-4d5c-ac83-558024322149",
                    False,
                ),
            },
        }.items():
            for name, (value, proxied) in records.items():
                create_record(
                    self,
                    zone_id=zone_id,
                    type=record_type,
                    name=name,
                    value=value,
                    proxied=proxied,
                )

        # GitHub Pages hexdoc books
        for page in github_pages:
            record.Record(
                self,
                f"GitHubPages_{page.name}_{page.value}",
                zone_id=zone_id,
                type="CNAME",
                name=page.name,
                value=page.value,
            )


def create_record(
    scope: Construct,
    *,
    zone_id: str,
    type: str,
    name: str | None,
    value: str,
    priority: int | None = None,
    proxied: bool = False,
    **kwargs: Any,
):
    match name:
        case "@":
            id_parts = [type, "ROOT", value]
        case "*":
            id_parts = [type, "WILDCARD", value]
        case str():
            id_parts = [type, name, value]
        case None:
            id_parts = [type, value]
            name = "@"

    return record.Record(
        scope,
        "_".join(id_parts).replace(".", "-"),
        zone_id=zone_id,
        type=type,
        name=name,
        value=value,
        priority=priority,
        proxied=proxied,
        **kwargs,
    )
