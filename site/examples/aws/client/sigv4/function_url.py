import Pyjo.AWS.Config
import Pyjo.AWS.Credentials.Chain
import Pyjo.AWS.SigV4
import Pyjo.UserAgent

import sys


if len(sys.argv) != 2:
    sys.exit('Usage: function_url.py https://abcdefghij.lambda-url.eu-central-1.on.aws')
base = sys.argv[1].rstrip('/')

# The region and the credentials that the AWS CLI finds, of the environment or of a profile
config = Pyjo.AWS.Config.new()
credentials = Pyjo.AWS.Credentials.Chain.new(config=config).credentials()

# The service of the signature: lambda of a Function URL of AWS_IAM, execute-api of API Gateway, es of OpenSearch
signer = Pyjo.AWS.SigV4.new(service='lambda', region=config.region(), credentials=credentials)

# Each request of the user agent, a redirect too, is signed once it is complete, before it is written
ua = Pyjo.UserAgent.new()
ua.on('start', lambda ua, tx: signer.sign(tx.req))

print(ua.get(f'{base}/hello/Sara').result.json())
print(ua.post(f'{base}/notes', json={'text': 'Hello!'}).result.json())
