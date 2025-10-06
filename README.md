# hexxy.media

Monorepo for https://hexxy.media/.

## Repository structure

- [.github/workflows/deploy.yml](./.github/workflows/deploy.yml): Deployment workflow for hexxy.media. Runs on every push to main.
- [codedeploy/](./codedeploy): Files in this directory are uploaded to S3 and deployed to the VPS. Some files are generated and added to this directory by the deployment workflow.
  - [appspec.yml](./codedeploy/appspec.yml): [AppSpec file](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html) for CodeDeploy. Configures where to copy files and what hooks to execute during a deployment.
  - [pm2.config.js](./codedeploy/pm2.config.js): [PM2 config file](https://pm2.keymetrics.io/docs/usage/application-declaration/) for the API.
- [src/azure/](./src/azure): [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) configs for Azure resources.
  - [main.bicepparam](./src/azure/main.bicepparam): Data-driven OIDC configuration to allow community members to publish packages to https://maven.hexxy.media via GitHub Actions.
- [src/hexxy_media/](./src/hexxy_media): Root directory for the `hexxy_media` Python package.
  - [api/](./src/hexxy_media/api): [FastAPI](https://fastapi.tiangolo.com/) source code for https://hexxy.media/api/v0/docs.
  - [common/](./src/hexxy_media/common): Dependency-free data and utilities for other packages.
    - [data.py](./src/hexxy_media/common/data.py): Primary source of truth for subdomains. This is used to generate a sitemap, DNS records, and the landing page at https://hexxy.media.
  - [web/](./src/hexxy_media/web): [Jinja](https://jinja.palletsprojects.com/en/stable/)-based static site generator for the landing page at https://hexxy.media.
- [src/infra/aws_cdk/](./src/infra/aws_cdk): [AWS CDK](https://aws.amazon.com/cdk/) application for hexxy.media. This deploys the [CodeDeploy application](https://docs.aws.amazon.com/codedeploy/latest/userguide/applications.html) and [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) that are used for deploying the API and landing page to the VPS that hosts them.
- [src/infra/cdktf/](./src/infra/cdktf): [CDKTF](https://developer.hashicorp.com/terraform/cdktf) (CDK for Terraform) application for hexxy.media. This deploys DNS records and [dynamic redirects](https://developers.cloudflare.com/rules/url-forwarding/single-redirects/) to Cloudflare for the hexxy.media domain.

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
