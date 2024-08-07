from dataclasses import dataclass, field


@dataclass(kw_only=True)
class GitHubPagesRecord:
    subdomain: str = field(kw_only=False)
    """hexxy.media subdomain.
    
    Usage: `https://{subdomain}.hexxy.media`
    """
    user: str
    """GitHub username.
    
    Usage: `https://{user}.github.io`
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
    def record_name(self):
        return self.subdomain

    @property
    def record_value(self):
        return f"{self.user.lower()}.github.io"

    @property
    def sortkey(self):
        return (
            0 if self.hoist else 1,
            self.title.lower(),
        )
