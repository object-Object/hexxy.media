import logging
import os
from dataclasses import dataclass
from typing import Any, Literal

import cdktf
from cdktf_cdktf_provider_cloudflare import provider, record
from cdktf_cdktf_provider_cloudflare.ruleset import (
    Ruleset,
    RulesetRules,
    RulesetRulesActionParameters as ActionParameters,
    RulesetRulesActionParametersFromValue as FromValue,
    RulesetRulesActionParametersFromValueTargetUrl as TargetUrl,
)
from constructs import Construct

from hexxy_media.common.types import GitHubPagesRecord


@dataclass
class IPWithPort:
    ip: str
    port: int


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

        # Cloudflare

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
            for name, (content, proxied) in records.items():
                create_record(
                    self,
                    zone_id=zone_id,
                    type=record_type,
                    name=name,
                    content=content,
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
                target="cypher-mc.hexxy.media",
                port=cypher_mc.port,
            ),
        )

        # root-level TXT records
        for content, ttl in [
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
                content=content,
                ttl=ttl,
            )

        # GitHub Pages hexdoc books
        for page in github_pages:
            record.Record(
                self,
                f"GitHubPages_{page.record_name}_{page.record_content}",
                zone_id=zone_id,
                type="CNAME",
                name=page.record_name,
                content=page.record_content,
            )

        # maven.hexxy.media
        Ruleset(
            self,
            "redirect_maven",
            zone_id=zone_id,
            name="maven",
            kind="zone",
            phase="http_request_dynamic_redirect",
            rules=[
                wildcard_redirect(
                    ref="root",
                    redirect_type="dynamic",
                    request_url="http*://maven.hexxy.media*",
                    target_url="https://pkgs.dev.azure.com/hexxy-media/artifacts/_packaging/public/maven/v1${2}",
                    status_code=301,
                    preserve_query_string=True,
                )
            ],
        )


def create_record(
    scope: Construct,
    *,
    zone_id: str,
    type: str,
    name: str | None,
    content: str,
    priority: int | None = None,
    proxied: bool = False,
    **kwargs: Any,
):
    match name:
        case "@":
            id_parts = [type, "ROOT", content]
        case "*":
            id_parts = [type, "WILDCARD", content]
        case str():
            id_parts = [type, name, content]
        case None:
            id_parts = [type, content]
            name = "@"

    return record.Record(
        scope,
        "_".join(id_parts).replace(".", "-"),
        zone_id=zone_id,
        type=type,
        name=name,
        content=content,
        priority=priority,
        proxied=proxied,
        **kwargs,
    )


def wildcard_redirect(
    *,
    ref: str,
    redirect_type: Literal["static", "dynamic"],
    request_url: str,
    target_url: str,
    status_code: int,
    preserve_query_string: bool | None = None,
):
    if redirect_type == "dynamic":
        target = TargetUrl(
            expression=f'wildcard_replace(http.request.full_uri, "{request_url}", "{target_url}")'
        )
    else:
        target = TargetUrl(value=target_url)

    return RulesetRules(
        ref=ref,
        expression=f'http.request.full_uri wildcard "{request_url}"',
        action="redirect",
        action_parameters=[
            ActionParameters(
                from_value=[
                    FromValue(
                        status_code=status_code,
                        preserve_query_string=preserve_query_string,
                        target_url=[target],
                    )
                ]
            )
        ],
    )
