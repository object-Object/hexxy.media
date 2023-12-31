from importlib.resources import Package

from hexdoc.__gradle_version__ import GRADLE_VERSION
from hexdoc.plugin import (
    HookReturn,
    LoadJinjaTemplatesImpl,
    LoadResourceDirsImpl,
    ModVersionImpl,
    hookimpl,
)

import hexdoc_hexxybook


class HexxyPlugin(
    LoadJinjaTemplatesImpl,
    LoadResourceDirsImpl,
    ModVersionImpl,
):
    @staticmethod
    @hookimpl
    def hexdoc_mod_version() -> str:
        return GRADLE_VERSION

    @staticmethod
    @hookimpl
    def hexdoc_load_resource_dirs() -> HookReturn[Package]:
        # This needs to be a lazy import because they may not exist when this file is
        # first loaded, eg. when generating the contents of generated.
        from ._export import generated

        return [generated]

    @staticmethod
    @hookimpl
    def hexdoc_load_jinja_templates() -> HookReturn[tuple[Package, str]]:
        return hexdoc_hexxybook, "_templates"
