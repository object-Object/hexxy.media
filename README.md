# HexxyAPI
Backend code for https://hexxy.media/api/v0/docs.

## Setup

```sh
python3.11 -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

## Run

```sh
source venv/bin/activate
python -m hexxyapi
```

## Deploy

```sh
source venv/bin/activate
pm2 start pm2.config.js
pm2 save
```
