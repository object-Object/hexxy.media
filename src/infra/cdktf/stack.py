import logging
import os
from dataclasses import dataclass
from typing import Any

import cdktf
from cdktf_cdktf_provider_cloudflare import provider, record
from constructs import Construct


@dataclass
class IPWithPort:
    ip: str
    port: int


@dataclass
class GitHubPagesRecord:
    subdomain: str
    github_user: str

    def __post_init__(self):
        if self.github_user != self.github_user.lower():
            raise ValueError(f"Invalid record {self}: github_user must be lowercase")

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
        objectobject_ca: str,
        hexxytest: str,
        cypher_mc: IPWithPort,
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
                "*": (objectobject_ca, True),
                "@": (objectobject_ca, True),
                "hexxytest": (hexxytest, False),
                "cypher-mc": (cypher_mc.ip, False),
            },
            "TXT": {
                "_dmarc": ("v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;", False),
                "*._domainkey": ("v=DKIM1; p=", False),
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

        # Minecraft SRV record for non-standard port
        record.Record(
            self,
            "SRV_cypher-mc",
            zone_id=zone_id,
            type="SRV",
            name="_minecraft._tcp",
            data=record.RecordData(
                service="_minecraft",
                proto="_tcp",
                name="cypher-mc",
                priority=10,
                weight=100,
                port=cypher_mc.port,
            ),
        )

        # root-level TXT records
        for value, ttl in [
            (
                "google-site-verification=NyyINfEEMwYz9RthiVwPJFn8-bIGMlEUMszznsLkNXQ",
                3600,
            ),
            ("v=spf1 -all", None),
        ]:
            create_record(
                self,
                zone_id=zone_id,
                type="TXT",
                name=None,
                value=value,
                ttl=ttl,
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
