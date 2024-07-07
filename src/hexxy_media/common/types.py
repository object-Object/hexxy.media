from dataclasses import dataclass


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
