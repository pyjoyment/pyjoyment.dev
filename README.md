[![Home](https://img.shields.io/badge/%F0%9F%8F%A0-Pyjoyment-02a7a0)](https://github.com/pyjoyment/Pyjoyment)
[![License](https://img.shields.io/github/license/pyjoyment/pyjoyment.dev.svg)](https://github.com/pyjoyment/pyjoyment.dev/blob/main/LICENSE)
[![Tests](https://github.com/pyjoyment/pyjoyment.dev/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/pyjoyment/pyjoyment.dev/actions/workflows/tests.yaml)
[![Trunk Check](https://github.com/pyjoyment/pyjoyment.dev/actions/workflows/trunk-check.yaml/badge.svg?branch=main)](https://github.com/pyjoyment/pyjoyment.dev/actions/workflows/trunk-check.yaml)

# pyjoyment.dev

The website of [Pyjoyment](https://github.com/pyjoyment/Pyjoyment), at
<https://pyjoyment.dev>: an application of Pyjoyment that runs as a function of
AWS Lambda behind CloudFront, with its static files and its dynamic pages.

## Running locally

The application is `site/app.py`, a script of `Pyjoyment.Lite`, with its
templates in `site/templates` and its static files in `site/public`:

```sh
uv run --directory site python app.py daemon
```

It listens on <http://127.0.0.1:3000>. The tests run it as a server and as the
function of Lambda:

```sh
uv run --project site python -m Pyjo.Prove -l -r t
```

## Building the function

`generate lambda-zip` writes `site/dist/function.zip`, with the application
alone, for the public layer of Pyjoyment of
[Pyjoyment-Lambda-Layers](https://github.com/pyjoyment/Pyjoyment-Lambda-Layers):

```sh
uv run --directory site python app.py generate lambda-zip --arch arm64 --runtime python3.15 --function-only
```

## Infrastructure

`tofu/` creates the function, its Function URL, the CloudFront distribution,
the certificate and the records of the domain in Cloudflare. It needs a
profile of AWS of the account `959435416781` and a token of the API of
Cloudflare, in `tofu/terraform.tfvars`:

```hcl
cloudflare_api_token = "..."
```

The first apply takes the function of the build above:

```sh
AWS_PROFILE=<profile> tofu -chdir=tofu init
AWS_PROFILE=<profile> tofu -chdir=tofu plan -out=tfplan
AWS_PROFILE=<profile> tofu -chdir=tofu apply tfplan
```

## License

Artistic License 2.0.
