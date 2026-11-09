import Pyjo.GCP.Config
import Pyjo.GCP.RSA

import sys
import time


# The key of a service account of GOOGLE_APPLICATION_CREDENTIALS, as gcloud iam service-accounts keys create makes it
config = Pyjo.GCP.Config.new()
info = config.credentials_info(config.credentials_file)
key = Pyjo.GCP.RSA.from_pem(info['private_key'])

# A JWT of RS256 of the service account for a service of its audience, as API Gateway, which verifies it with the
# public keys of the service account; the ID of the key, in the header, tells which one
now = int(time.time())
claims = {'iss': info['client_email'], 'sub': info['client_email'], 'aud': sys.argv[1], 'iat': now, 'exp': now + 3600}
print(key.jwt(claims, key_id=info['private_key_id']))
