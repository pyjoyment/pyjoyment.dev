# Agent Guide: pyjoyment.dev

## Overview

The repository is the website of Pyjoyment, `pyjoyment.dev`: an application
of Pyjoyment, its static files and its dynamic pages, which runs as an event
function of AWS Lambda behind CloudFront, and the OpenTofu of its
infrastructure. It is not a distribution: it installs nothing of its own. The
conventions are those of Pyjoyment: read its `AGENTS.md` in the checkout next
to this one, `../Pyjoyment/AGENTS.md`.

## Layout

- `site/`: the application, and only the application, as
  `generate lambda-zip` puts every file of the current directory into
  `function.zip`, but the hidden ones, `__pycache__` and `dist`. It is a
  project of uv of its own, with `pyproject.toml` and `uv.lock`, which the
  generator reads in the directory of the application, so the tests, the
  configuration of the linters and the infrastructure are outside of it.
- `t/`: the tests.
- `tofu/`: the infrastructure.
- `deploy.py`: the deployment of the function, outside of `site/`, so that it
  is not in the function.

The configuration of ruff and pyright is in the root of the repository, in
`ruff.toml` and `pyrightconfig.json`, for `site/` and `t/` alike: ruff skips a
`pyproject.toml` without `[tool.ruff]`, as the one of `site/`, and
`pyrightconfig.json` names the environment of `uv sync` of `site/`. The
commands of uv take the project of `site/` with `--project site` from the root,
or run in `site/`.

## The Application

`site/app.py` is a script of `Pyjoyment.Lite`, whose last line,
`handler = app.start()`, is the handler `app.handler` of the function and runs
the command of its arguments otherwise, as `daemon`.

CloudFront caches what the application says with `Cache-Control`, and nothing
else. In the mode `production`, the one of the function, the hook
`after_static` and the pages of the showcase, after they are rendered, so that
the page of an exception is not cached, give `public, max-age=3600,
s-maxage=604800`: a week of CloudFront, which the invalidation of `/*` of each
deployment ends, and an hour of the browsers, which it does not reach. In
another mode, as the development of `daemon` and `reload`, they give
`no-cache`, so that a change is seen at once. A response of an action without
the header, as `/hello`, is not cached in any mode.

### The Showcase

The page is a showcase of Pyjoyment: the buttons of the features and of the
roles, a scenario of the feature and the role, and the tabs of the files of
the scenario. `site/examples/catalog.yaml` lists the features, the roles and
the scenarios of each feature and role, and the files of a scenario are in
`site/examples/<feature>/<role>/<scenario>/`. One role at a time, without the
pairs of roles, as a scenario of two roles mixes two examples in one. A
scenario without its directory is shown as coming soon, and a feature or a
role that leads to no scenario is dimmed. The application reads the catalog
and the files at its start, and fails on a feature or a role of the catalog
that is not one of its lists, or a file of `files` that is missing.

Each selection is a page of its own, `/http`, `/server`, `/http/server`,
`/http/server/lambda`, rendered by `page` of `site/app.py`, so the page works
without JavaScript and a test reads it as any page. A button selects its
feature or role in place of the one selected, and the one selected unselects
it. `public/js/site.js` swaps `<main>` with the one of the page of a link
instead of loading it, and draws the link between the selected feature and
role in SVG. The footer is outside of `<main>`, so it stays as the script
swaps the page, and its badges, `BADGES` of `site/app.py`, are the images of
shields.io. The other files of another host are those of Google Tag Manager,
`GTM-5NGTPTM6`, which the layout loads in the mode `production` only, so that
the development and the tests of the server send nothing to Google Analytics.
A swap of `<main>` is a change of the history of the browser, not a load of a
page, which the container of GTM counts as a page view only with a trigger of
the changes of the history, or the enhanced measurement of GA4 that has one.

The examples are scripts, and ruff checks them with the exceptions of the
scripts of `Pyjoyment.Lite` and of the tests, but pyright does not, with
`ignore` of `pyrightconfig.json`, as they import libraries that the
environment of `site/` does not have, as Django, Flask, Pyjo-GCP or Pyjo-MCP.
The site runs on the Pyjoyment of `uv.lock`, a revision of main, for the
precompressed static files, until a release has them, while the examples,
which the site shows and does not run, may describe the next release, as
0.4.0, before it, and are reviewed again after it. A template of the site
takes no `% else:` right after the `% end` of a loop in an `if`, which
Pyjoyment 0.3.0 fails on (pyjoyment/Pyjoyment#575, fixed for 0.4.0), so the
template of the page puts the branch without a loop first.
A file whose real name is hidden, as `.mcp.json`, is in the directory of its
scenario without its dot, with its real name as its `title` in the catalog,
as `list_tree` and `generate lambda-zip` leave the hidden files out. `t/examples.py` compiles each
example of Python without running it, as most of them need a cloud or another
server, so an example that a test cannot run is still Python. highlight.js is in
`public/vendor/highlight.js`, as its release minified it, which `biome.jsonc`
leaves out, with the languages that its common build does not have in
`languages/`, which the layout loads. `LANGUAGES` of `site/app.py` gives the
language of a file by its name or its extension, and `language` of a file in
the catalog the one that neither tells, as `nginx` for `nginx.conf`.
HCL of the files `.tf`, which highlight.js has not, is the grammar of
`public/js/hcl.js`, of this site, instead of a third-party one.

The function gets the requests with the host of its Function URL, not
`pyjoyment.dev`, as the Function URL takes the requests of its own host only,
so the application makes relative URLs, as `url_for` does by default, and not
absolute ones of the host of the request.

The distribution takes `GET`, `HEAD` and `OPTIONS` only. The origin access
control of a Function URL takes a request with a body only with the SHA-256
of the body in `x-amz-content-sha256`, which the client computes, so a form or
an API that posts needs another way before the distribution takes `POST`.

## Building

`generate lambda-zip --no-layer` writes `site/dist/function.zip`, the
application with the Pyjoyment of `uv.lock`, a revision of main, which no
public layer of Pyjoyment-Lambda-Layers has, for the runtime of Python of
Lambda, as the workflow Build does:

```sh
mise exec -- uv run --directory site python app.py generate lambda-zip --arch arm64 --runtime python3.15 --no-layer --compress public --compress Pyjoyment/resources/public
```

The runtime, `python3.15`, and the architecture, `arm64`, are the same in the
workflow and in `tofu/`. `--compress` writes the precompressed variants of
the static files, `.br`, `.zst` and `.gz`, which `Pyjoyment.Static` serves
with `Vary: Accept-Encoding`, of `public/` and of the resources of Pyjoyment,
as the logo, which are in the function with Pyjoyment. The `.br` needs the
command `brotli`, which the workflow installs if the runner has none: without
it, a client of brotli gets `.gz`, which CloudFront, whose `compress` takes
only a response without `Content-Encoding`, does not compress again.
CloudFront forwards `Accept-Encoding` normalized to `br` and `gzip`, so the
`.zst` are in the function and are not served through it.

After a release of Pyjoyment with the precompressed static files and its
layers, `uv.lock` takes it from PyPI, and the build may take
`--function-only` again, with the layer instead of Pyjoyment in the function.

## Deployment

The job Deploy of the workflow Build deploys the build of a push to `main`,
or of a dispatch on `main`, with `deploy.py`, in the environment `production`,
which takes `main` only and waits for no approval, as the code on `main` comes
through pull requests:

```sh
AWS_PROFILE=<profile> mise exec -- uv run --project site python deploy.py --distribution E3L54LJQ60FS5U site/dist/function.zip
```

`deploy.py` calls the APIs of AWS with `Pyjo.AWS.Client` of Pyjo-AWS, as
Pyjoyment-Lambda-Layers does, instead of the AWS CLI: it is the dependency of
the group `dev` of `site/`, which `uv export --no-dev` of
`generate lambda-zip` leaves out of the function, which does not use it. It takes the credentials that the AWS CLI finds, of the
environment, which `aws-actions/configure-aws-credentials` sets, or of a
profile.

A `function.zip` with Pyjoyment of its own, of `--no-layer`, goes first, and
the function loses its layer after, as the code before needs it. For a
`function.zip` of `--function-only`, it gives the function the layer of the
Pyjoyment of `uv.lock`, by its name in the index of the latest release of
Pyjoyment-Lambda-Layers, as `pyjoyment-0_3_0-python3_15` for the runtime of
the function, not the alias of the latest Pyjoyment, `pyjoyment-python3_15`,
which the first apply of `tofu/` takes: a bump of Pyjoyment in `uv.lock`
before its layers are released
fails the deployment, instead of running the application on another
Pyjoyment. The index has the layers of its release only, so a `uv.lock` of an
older Pyjoyment fails too. The layer goes before the code, as the code of a
newer Pyjoyment needs its layer, where a newer layer runs the code of the one
before, and each update waits until `LastUpdateStatus` of the function is
`Successful`, as Lambda takes no other update before.

The deployment invalidates `/*` of the distribution at last, the files of
`public/` that CloudFront keeps for an hour, which is one path of the free
thousand of a month.

## The Infrastructure

`tofu/` is the infrastructure of the account `959435416781`, in `us-east-1`,
as CloudFront takes its certificate from there only: the function, its role
and its log group, its Function URL, the CloudFront distribution with its
origin access control and its cache policy, the certificate of ACM, the role
of the deployment, and the records of `pyjoyment.dev` in Cloudflare, which has
the zone. It is applied by
hand, never by CI, with the credentials of `AWS_PROFILE`, and
`allowed_account_ids` of the provider stops a profile of another account
before it changes anything:

```sh
cd tofu
AWS_PROFILE=<profile> mise exec -- tofu init
AWS_PROFILE=<profile> mise exec -- tofu plan -out=tfplan
AWS_PROFILE=<profile> mise exec -- tofu apply tfplan
```

The state is in the bucket of the state of Pyjoyment-Lambda-Layers,
`pyjoyment-tofu-state-959435416781`, under the key
`pyjoyment.dev/terraform.tfstate`.

The token of the API of Cloudflare is the variable `cloudflare_api_token` in
`tofu/terraform.tfvars`, which git ignores. It has `Zone:Read`, for the lookup
of the zone, and `Zone:DNS:Edit`, for its records, of the zone `pyjoyment.dev`
only. The records point at CloudFront without the proxy of Cloudflare, as the
distribution is the CDN, and the one of the apex is a CNAME, which Cloudflare
flattens.

The Function URL has `authorization_type = "AWS_IAM"` and takes only the
requests that the distribution signs with its origin access control, which
the function allows with both actions that a Function URL needs,
`lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` of the Function URL, for
the ARN of the distribution only, so nobody passes by the distribution. The
origin request policy is the managed one of all the headers of the viewer but
`Host`, which the Function URL needs to be its own.

The configuration creates the function with the first build of
`site/dist/function.zip`. A deployment of the application changes the code and
the layer of the function outside of OpenTofu, which ignores them, so that a
plan needs no build and does not take a deployment back.

A document of a policy takes no attribute of another resource, as in
Pyjoyment-Lambda-Layers: such a value is unknown until the apply, and the plan
shows the document as `(known after apply)` instead of its statements. The
documents build the ARNs from the account and the name of the function
instead, and the role of the deployment invalidates every distribution of the
account, which has this one only, as the ID of a distribution is unknown until
it is created.

The role `pyjoyment-dev-deploy` of the deployment is assumed by the jobs of
the environment `production` of this repository only, with the immutable
subject of its OIDC tokens, with the IDs of its owner and of itself,
`repo:pyjoyment@351424207/pyjoyment.dev@1448381496`, so that a repository of
the same name made anew does not get the role. The OIDC provider of GitHub is
the one of the account, of Pyjoyment-Lambda-Layers, which manages it, as an
account has one provider of a URL.

## Tests

The tests are scripts of `Pyjo.Test` in `t`, which `Pyjo.Prove` runs, on the
reactor of asyncio and on the one of poll, in the development mode of Python,
as the workflow Tests does:

```sh
PYTHONDEVMODE=1 mise exec -- uv run --project site python -m Pyjo.Prove -l --capture-stderr -r t
PYJO_REACTOR=Pyjo.Reactor.Poll PYTHONDEVMODE=1 mise exec -- uv run --project site python -m Pyjo.Prove -l --capture-stderr -r t
```

`t/site.py` runs the application as a server, and as the function with the
events of a Function URL, with `Pyjo.App.Lambda`, as Lambda runs it.

## Development

```sh
mise install
mise exec -- uv sync --project site
```

Trunk checks the files with the linters of Pyjoyment, from
`.trunk/trunk.yaml`:

```sh
trunk check --all --no-fix
```

actionlint is the one of the maintained fork kjanat/actionlint, as in
Pyjoyment: `downloads` in `.trunk/trunk.yaml` replaces the URLs of the plugin
with those of the fork, whose files have the same names.

Biome formats and lints CSS, HTML, JSON, Markdown and YAML, with
`biome.jsonc`, and yamllint checks what Biome does not, as the duplicated
keys. The version of Biome is the pinned one of `.trunk/trunk.yaml`, where `!`
keeps it from `trunk upgrade`, and which Renovate bumps: the repository has no
`package.json`. The workflow Biome Migrate migrates `biome.jsonc` and formats
the files on the branch of Renovate, as in Pyjoyment, whose `AGENTS.md` says
why.

tflint checks `tofu/` with the rules of its plugins `terraform` and `aws`,
from `.tflint.hcl` in the root of the repository, where the extensions of the
editors find it, which the definition of tflint in `.trunk/trunk.yaml` names
in `TFLINT_CONFIG_FILE`. `tflint --init` downloads the plugins from the
releases of GitHub, whose API limits the requests without a token, so Trunk
Check of CI has `GITHUB_TOKEN`, and a local run that fails with the limit of
the API takes the one of `gh`:

```sh
GITHUB_TOKEN=$(gh auth token) trunk check --all --no-fix
```

Renovate does not bump the providers of `tofu/` nor its `required_version`,
as the configuration is applied by hand: the providers and their lock are
upgraded when it is applied.

The workflows that start the checks of a commit of the token of a workflow, as
Automated trunk upgrade and Biome Migrate, start every check that the ruleset
of `main` requires: a new required check is added to them too.

## Security

Never read, display, reference, or include the contents of the following
files:

- `.env`, `.env.*`, `.envrc`
- `.pypirc`
- `*.tfvars`, as `tofu/terraform.tfvars` with the token of Cloudflare
- `*.jks`, `*.keystore`, `*.p12`, `*.pfx`, `*.pem`, `*.key`

The same list is git-ignored in `.gitignore`, and the rules of
`permissions.deny` of `.claude/settings.json` enforce it for Claude Code, as
in Pyjoyment: change all three together.

## Commits and Pull Requests

As in Pyjoyment: short subjects in the style of the history, mechanical and
functional changes in separate commits, and a pull request with a validation
checklist, checked only once verified.
