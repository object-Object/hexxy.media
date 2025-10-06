from dataclasses import dataclass, field


@dataclass(kw_only=True)
class LinkRecord:
    subdomain: str = field(kw_only=False)
    """hexxy.media subdomain.
    
    Usage: `https://{subdomain}.hexxy.media`
    """
    title: str = ""
    """Title displayed on the generated website.
    
    If not set, defaults to the subdomain in sentence case.
    """
    hoist: bool = False
    """If True, display above all other links on the generated website."""

    def __post_init__(self):
        self.subdomain = self.subdomain.lower()

        if not self.title:
            self.title = self.subdomain.capitalize()

    @property
    def url(self):
        return f"https://{self.subdomain}.hexxy.media"

    @property
    def sortkey(self):
        return (
            0 if self.hoist else 1,
            self.title.lower(),
        )


@dataclass(kw_only=True)
class GitHubPagesRecord(LinkRecord):
    user: str
    """GitHub username.
    
    Usage: `https://{user}.github.io`
    """

    @property
    def record_name(self):
        return self.subdomain

    @property
    def record_content(self):
        return f"{self.user.lower()}.github.io"
