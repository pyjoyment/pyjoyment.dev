"""
deploy.py - Deployment of pyjoyment.dev
=======================================
::

    python deploy.py --distribution E3L54LJQ60FS5U site/dist/function.zip

Updates the function with ``function.zip`` of ``generate lambda-zip``, and
its layer: the one of Pyjoyment of the version of ``uv.lock``, for the
runtime of the function, for a ZIP of ``--function-only``, or none for a ZIP
with Pyjoyment of its own, of ``--no-layer``, and invalidates the files that
CloudFront keeps, with :mod:`Pyjo.AWS.Client`, with the credentials that the
AWS CLI finds, of the environment, as those of the OIDC of GitHub Actions, or
of a profile of ``AWS_PROFILE``.
"""

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.Query
import Pyjo.AWS.Protocol.RestJSON
import Pyjo.AWS.Protocol.RestXML
import Pyjo.DOM
import Pyjo.Exception
import Pyjo.File
import Pyjo.Log
import Pyjo.UserAgent

from Pyjo.Util import b64_encode, getopt

import importlib.metadata
import sys
import time
import zipfile

from typing import Any


LAYERS = 'https://github.com/pyjoyment/Pyjoyment-Lambda-Layers/releases/latest/download/layers.json'
REGION = 'us-east-1'


def configuration(aws: Pyjo.AWS.Client.object, function: str) -> dict[str, Any]:
    return aws.call(Pyjo.AWS.Protocol.RestJSON.new('GET', f'/2015-03-31/functions/{function}/configuration'))


# An update of a function is done when Lambda says so, and the next one fails with 409 before
def updated(aws: Pyjo.AWS.Client.object, function: str) -> dict[str, Any]:
    for _ in range(60):
        config = configuration(aws, function)
        status = config.get('LastUpdateStatus')
        if status == 'Successful':
            return config
        if status == 'Failed':
            raise Pyjo.Exception.new(f'The update of {function} failed: {config.get("LastUpdateStatusReason")}')
        time.sleep(2)
    raise Pyjo.Exception.new(f'The update of {function} is not done after two minutes')


# The layer of the Pyjoyment of uv.lock, which the generator left out of the function, as pyjoyment-0_3_0-python3_15,
# not the alias of the latest Pyjoyment, so that a Pyjoyment without its layer yet fails the deployment
def layer(ua: Pyjo.UserAgent.object, runtime: str) -> str:
    version = importlib.metadata.version('Pyjoyment')
    name = f'pyjoyment-{version}-{runtime}'.replace('.', '_')
    layers = ua.get(LAYERS).result.json()
    if not (arn := layers.get(name, {}).get(REGION)):
        raise Pyjo.Exception.new(f'No layer {name} in {REGION} in the latest release of Pyjoyment-Lambda-Layers')
    return arn


def layers(aws: Pyjo.AWS.Client.object, function: str, arns: list[str], log: Pyjo.Log.object) -> None:
    call = Pyjo.AWS.Protocol.RestJSON.new(
        'PUT', f'/2015-03-31/functions/{function}/configuration', json={'Layers': arns}
    )
    aws.call(call)
    updated(aws, function)
    log.info(f'[layer] {function} {" ".join(arns) or "none"}')


# The XML of the batch, with the elements of new_tag, which escapes their text, in XML, which keeps the case of their
# names
def invalidation(reference: str) -> Pyjo.DOM.object:
    dom = Pyjo.DOM.new()
    dom.xml = True
    tag = dom.new_tag
    items = tag('Items').at('Items').append_content(tag('Path', '/*')).root
    paths = tag('Paths').at('Paths').append_content(tag('Quantity', '1')).append_content(items).root
    batch = tag('InvalidationBatch', xmlns='http://cloudfront.amazonaws.com/doc/2020-05-31/').at('InvalidationBatch')
    return batch.append_content(paths).append_content(tag('CallerReference', reference)).root


def main(args: list[str]) -> None:
    if not (opts := getopt(args, {'d|distribution=s': None, 'f|function=s': None})) or len(args) != 1:
        sys.exit(__doc__)
    function = opts.function or 'pyjoyment-dev'
    path = Pyjo.File.new(args[0])
    log = Pyjo.Log.new()

    # layers.json is behind a redirection of GitHub
    ua = Pyjo.UserAgent.new(max_redirects=3)
    aws = Pyjo.AWS.Client.new(service='lambda', region=REGION, ua=ua)

    # The identity first, so that the log shows the account and the role of the deployment; the clients share the
    # credentials, so that those of a profile are read once
    sts = Pyjo.AWS.Client.new(service='sts', region=REGION, credentials=aws.credentials, ua=ua)
    dom = sts.call(Pyjo.AWS.Protocol.Query.new('GetCallerIdentity', version='2011-06-15'))
    log.info(f'[identity] {dom.at("Account").text} {dom.at("Arn").text}')

    # A ZIP of --no-layer has Pyjoyment of its own, which no layer has, as one of main before its release
    own = 'Pyjoyment/__init__.py' in zipfile.ZipFile(path.to_str()).namelist()
    config = configuration(aws, function)
    # Layers is null for a function without layers, not missing
    current = [item['Arn'] for item in config.get('Layers') or []]
    arns = [] if own else [layer(ua, config['Runtime'])]

    # The layer before the code, as the code of a newer Pyjoyment needs it, where a newer layer serves the code before;
    # a code with Pyjoyment of its own goes before the layer is removed, as the code before needs the layer
    if not own and current != arns:
        layers(aws, function, arns, log)

    call = Pyjo.AWS.Protocol.RestJSON.new(
        'PUT', f'/2015-03-31/functions/{function}/code', json={'ZipFile': b64_encode(path.slurp(), '')}
    )
    aws.call(call)
    config = updated(aws, function)
    log.info(f'[code] {function} {config["CodeSha256"]}')

    if own and current != arns:
        layers(aws, function, arns, log)

    # The files of public/ that CloudFront keeps for an hour; the wildcard is one path of the free thousand of a month
    if opts.distribution:
        cloudfront = Pyjo.AWS.Client.new(
            service='cloudfront',
            endpoint='https://cloudfront.amazonaws.com',
            region=REGION,
            credentials=aws.credentials,
            ua=ua,
        )
        body = invalidation(config['RevisionId']).to_str()
        call = Pyjo.AWS.Protocol.RestXML.new('POST', f'/2020-05-31/distribution/{opts.distribution}/invalidation', body)
        dom = cloudfront.call(call)
        log.info(f'[invalidation] {opts.distribution} {dom.at("Invalidation > Id").text}')


if __name__ == '__main__':
    main(sys.argv[1:])
