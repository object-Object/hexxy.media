import logging
from pathlib import Path

import sass
from jinja2 import Environment, PackageLoader, StrictUndefined

from hexxy_media.common.data import GITHUB_PAGES_MOD_BOOKS, GITHUB_PAGES_RECORDS

logger = logging.getLogger(__name__)


def build_jinja(output_dir: Path, *, hot_reload: bool):
    logger.info("Building website with Jinja.")

    env = Environment(
        loader=PackageLoader("hexxy_media.web", "templates"),
        undefined=StrictUndefined,
        lstrip_blocks=True,
        trim_blocks=True,
        autoescape=False,
    )

    templates = {
        "index.html": "index.html.jinja",
        "index.css": "index.scss.jinja",
    }

    template_args = {
        "github_pages_records": GITHUB_PAGES_RECORDS,
        "github_pages_mod_books": GITHUB_PAGES_MOD_BOOKS,
        "hot_reload": hot_reload,
    }

    for output_file, template_name in templates.items():
        output_path = output_dir / output_file
        logger.info(f"Rendering template {template_name} to {output_path}.")

        template = env.get_template(template_name)
        output = template.render(template_args)

        if template_name.endswith((".scss", ".scss.jinja")):
            logger.info(f"Compiling output of template {template_name} with Sass.")
            output = sass.compile(string=output)

        output_path.write_text(output, "utf-8")
