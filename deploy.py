"""
deploy.py - Deployment of pyjoyment.dev
=======================================
::

    python deploy.py --distribution E3L54LJQ60FS5U site/dist/function.zip

Updates the function with ``function.zip`` of ``generate lambda-zip
--function-only`` and the layer of Pyjoyment of the version of ``uv.lock``,
for the runtime of the function, and invalidates the files that CloudFront
keeps, with :mod:`Pyjo.AWS.Client`, with the credentials that the AWS CLI
finds, of the environment, as those of the OIDC of GitHub Actions, or of a
profile of ``AWS_PROFILE``.
"""

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.RestJSON
import Pyjo.AWS.Protocol.RestXML
import Pyjo.Exception
import Pyjo.File
import Pyjo.UserAgent

from Pyjo.Util import b64_encode, getopt

import importlib.metadata
import sys
import time

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


def invalidation(reference: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<InvalidationBatch xmlns="http://cloudfront.amazonaws.com/doc/2020-05-31/">
  <Paths><Quantity>1</Quantity><Items><Path>/*</Path></Items></Paths>
  <CallerReference>{reference}</CallerReference>
</InvalidationBatch>
"""


def main(args: list[str]) -> None:
    if not (opts := getopt(args, {'d|distribution=s': None, 'f|function=s': None})) or len(args) != 1:
        sys.exit(__doc__)
    function = opts.function or 'pyjoyment-dev'
    path = Pyjo.File.new(args[0])

    # layers.json is behind a redirection of GitHub
    ua = Pyjo.UserAgent.new(max_redirects=3)
    aws = Pyjo.AWS.Client.new(service='lambda', region=REGION, ua=ua)

    config = configuration(aws, function)
    arn = layer(ua, config['Runtime'])

    # The layer before the code, as the code of a newer Pyjoyment needs it, where a newer layer serves the code before
    if [current['Arn'] for current in config.get('Layers', [])] != [arn]:
        call = Pyjo.AWS.Protocol.RestJSON.new(
            'PUT', f'/2015-03-31/functions/{function}/configuration', json={'Layers': [arn]}
        )
        aws.call(call)
        updated(aws, function)
        print(f'[layer] {function} {arn}')

    call = Pyjo.AWS.Protocol.RestJSON.new(
        'PUT', f'/2015-03-31/functions/{function}/code', json={'ZipFile': b64_encode(path.slurp(), '')}
    )
    aws.call(call)
    config = updated(aws, function)
    print(f'[code] {function} {config["CodeSha256"]}')

    # The files of public/ that CloudFront keeps for an hour; the wildcard is one path of the free thousand of a month
    if opts.distribution:
        cloudfront = Pyjo.AWS.Client.new(
            service='cloudfront', endpoint='https://cloudfront.amazonaws.com', region=REGION, ua=ua
        )
        body = invalidation(config['RevisionId'])
        call = Pyjo.AWS.Protocol.RestXML.new('POST', f'/2020-05-31/distribution/{opts.distribution}/invalidation', body)
        dom = cloudfront.call(call)
        print(f'[invalidation] {opts.distribution} {dom.at("Invalidation > Id").text}')


if __name__ == '__main__':
    main(sys.argv[1:])
