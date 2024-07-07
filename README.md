# hexxy.media

Monorepo for https://hexxy.media/.

## Adding a subdomain

Hex Casting addons are welcome to freely use `{modid}.hexxy.media` for their GitHub Pages web books or any other (reasonable) purpose.

To register a subdomain for GitHub Pages, you can open a pull request adding a record to the appropriate list in [`src/hexxy_media/common/data.py`](src/hexxy_media/common/data.py), or just open an issue / ping me on Discord (`@leftsquarebracket`).

## Setup

```sh
python3.11 -m venv venv
source venv/bin/activate
pip install -e .[dev]
npm i
```

Create a file called `.env`:
```
DB_HOST=localhost
DB_PORT=...
DB_USER=hexxy_media
DB_PASS=...
DB_NAME=hexxy_media
```

## Run locally

`DB_PORT=63333`

Terminal 1:
```sh
ssh -L 63333:localhost:5432 object@objectobject.ca -N
```

Terminal 2:
```sh
source venv/bin/activate
uvicorn --reload --port 5000 hexxy_media.api.app:app
```

## Run static site locally

```sh
nodemon
```

## Deploy

Deployments are performed automatically on push via GitHub Actions, AWS CDK, CDKTF, and CodeDeploy.
