# hexdoc-hexxybook

Python web book docgen and [hexdoc](https://pypi.org/project/hexdoc) plugin for the [Book of Hexxy](https://book.hexxy.media/). This is a meta-book that includes content from as many other hexdoc books as possible.

## Usage

For local testing, create a file called `.env` in the repo root following this template:
```sh
GITHUB_REPOSITORY=object-Object/hexxy.media
GITHUB_SHA=main
GITHUB_PAGES_URL=https://book.hexxy.media/
```

Then run these commands to generate the book:
```sh
# run from the repo root, not doc/
hexdoc render
hexdoc merge
```

Or, run this command to render the book and start a local web server:
```sh
hexdoc serve --lang en_us
```
