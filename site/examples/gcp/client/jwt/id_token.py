import Pyjo.GCP.Call
import Pyjo.GCP.Client
import Pyjo.UserAgent

import sys


# A Cloud Run service that takes authenticated requests only, of a service account with the role Cloud Run Invoker,
# which the credentials impersonate with the role Service Account Token Creator on it
url, account = sys.argv[1:3]

# An ID token of Google, a JWT of the service account whose audience is the URL of the service, of the IAM Service
# Account Credentials API; on Cloud Run or Compute Engine, the metadata server gives one of its own service account
iam = Pyjo.GCP.Client.new(service='iamcredentials')
call = Pyjo.GCP.Call.new(
    'POST', f'/v1/projects/-/serviceAccounts/{account}:generateIdToken', {'audience': url, 'includeEmail': True}
)
token = iam.call(call)['token']

print(Pyjo.UserAgent.new().get(url, {'Authorization': f'Bearer {token}'}).result.text)
