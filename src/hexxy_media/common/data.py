from .types import GitHubPagesRecord

# generates CNAME records from `{subdomain}.hexxy.media` to `{github_user}.github.io`
# NOTE: all fields must be lowercase

GITHUB_PAGES_RECORDS = [
    GitHubPagesRecord(subdomain="hexdoc", github_user="hexdoc-dev"),
    GitHubPagesRecord(subdomain="addons", github_user="samsthenerd"),
    GitHubPagesRecord(subdomain="book", github_user="hexdoc-dev"),
]

GITHUB_PAGES_MOD_BOOKS = [
    GitHubPagesRecord(subdomain="hexcasting", github_user="fallingcolors"),
    GitHubPagesRecord(subdomain="hexgloop", github_user="samsthenerd"),
    GitHubPagesRecord(subdomain="oneironaut", github_user="beholderface"),
    GitHubPagesRecord(subdomain="ephemera", github_user="beholderface"),
    GitHubPagesRecord(subdomain="hexdebug", github_user="object-object"),
    GitHubPagesRecord(subdomain="hexbound", github_user="object-object"),
]
