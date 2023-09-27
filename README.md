# HexxyAPI
Backend code for https://hexxy.media/api/v0/docs.

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
ssh -L 63333:localhost:5432 object@objectobject.ca
```

Terminal 2:
```sh
source venv/bin/activate
python -m hexxyapi
```

## Deploy

`DB_PORT=5432`

```sh
source venv/bin/activate
pm2 start pm2.config.js
pm2 save
```
