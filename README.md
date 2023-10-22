# hexxy.media
Monorepo for https://hexxy.media/.

## Setup

```sh
python3.11 -m venv venv
source venv/bin/activate
pip install -e .[dev]
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
python -m hexxy_media.api.app
```

## Deploy

Deployments are performed automatically on push via GitHub Actions, AWS CDK, CDKTF, and CodeDeploy.
