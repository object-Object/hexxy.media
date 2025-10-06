from .types import GitHubPagesRecord, LinkRecord

# representation of manually added records for sitemap and generated website

LINK_RECORDS = [
    LinkRecord("hexxytest", title="HexxyTest"),
    LinkRecord("maven"),
]

# generates CNAME records from `{subdomain}.hexxy.media` to `{user}.github.io`

GITHUB_PAGES_RECORDS = [
    GitHubPagesRecord("addons", user="SamsTheNerd", title="Hex Casting Additions"),
    GitHubPagesRecord("hexdoc", user="hexdoc-dev", title="hexdoc"),
]

# parameters:
# - subdomain (the first string): Subdomain name, eg. "book" creates the subdomain `book.hexxy.media`
# - user: GitHub username owning the repository that is using GitHub Pages.
# - title: Display name used on hexxy.media. Defaults to the subdomain with the first letter capitalized.
# - hoist: If True, display on hexxy.media in a separate group from the rest of the links.
GITHUB_PAGES_MOD_BOOKS = [
    GitHubPagesRecord("book", user="object-Object", title="Book of Hexxy", hoist=True),
    GitHubPagesRecord(
        "hexcasting", user="FallingColors", title="Hex Casting", hoist=True
    ),
    GitHubPagesRecord("hexal", user="FallingColors"),
    GitHubPagesRecord("moreiotas", user="FallingColors", title="MoreIotas"),
    GitHubPagesRecord("ephemera", user="beholderface"),
    GitHubPagesRecord("hexgloop", user="SamsTheNerd", title="Hex Gloop"),
    GitHubPagesRecord("caduceus", user="object-Object"),
    GitHubPagesRecord("hexbound", user="object-Object"),
    GitHubPagesRecord("hexdebug", user="object-Object", title="HexDebug"),
    GitHubPagesRecord("ioticblocks", user="object-Object", title="IoticBlocks"),
    GitHubPagesRecord("oneironaut", user="beholderface"),
    GitHubPagesRecord("complexhex", user="kineticneticat", title="Complex Hex"),
    GitHubPagesRecord("hexical", user="miyucomics"),
    GitHubPagesRecord("hexcellular", user="miyucomics"),
    GitHubPagesRecord(
        "hextended", user="abilliontrillionstars", title="Hextended Staves"
    ),
]
