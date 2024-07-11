from .types import GitHubPagesRecord

# generates CNAME records from `{subdomain}.hexxy.media` to `{user}.github.io`

GITHUB_PAGES_RECORDS = [
    GitHubPagesRecord("addons", user="SamsTheNerd", title="Hex Casting Additions"),
    GitHubPagesRecord("hexdoc", user="hexdoc-dev", title="hexdoc"),
]

GITHUB_PAGES_MOD_BOOKS = [
    GitHubPagesRecord("book", user="hexdoc-dev", title="Book of Hexxy", hoist=True),
    GitHubPagesRecord(
        "hexcasting", user="FallingColors", title="Hex Casting", hoist=True
    ),
    GitHubPagesRecord("ephemera", user="beholderface"),
    GitHubPagesRecord("hexgloop", user="SamsTheNerd", title="Hex Gloop"),
    GitHubPagesRecord("hexbound", user="object-Object"),
    GitHubPagesRecord("hexdebug", user="object-Object", title="HexDebug"),
    GitHubPagesRecord("oneironaut", user="beholderface"),
    GitHubPagesRecord("complexhex", user="kineticneticat", title="Complex Hex"),
]

ALL_GITHUB_PAGES_RECORDS = GITHUB_PAGES_RECORDS + GITHUB_PAGES_MOD_BOOKS
