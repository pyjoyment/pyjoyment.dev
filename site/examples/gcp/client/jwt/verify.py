import Pyjo.GCP.RSA
import Pyjo.JSON
import Pyjo.UserAgent

from Pyjo.Util import b64url_decode, url_escape

import sys
import time


token, audience = sys.argv[1:3]
header, payload, signature = token.split('.')
head, claims = (Pyjo.JSON.decode_json(b64url_decode(part)) for part in (header, payload))

# The public keys of Google, of its ID tokens, or the ones of the service account that signed the JWT with its key
if claims['iss'] in ('https://accounts.google.com', 'accounts.google.com'):
    url = 'https://www.googleapis.com/oauth2/v3/certs'
else:
    url = 'https://www.googleapis.com/service_accounts/v1/jwk/' + url_escape(claims['iss'], r'^A-Za-z0-9\-._~@')
keys = {key['kid']: key for key in Pyjo.UserAgent.new().get(url).result.json('/keys')}

if head.get('alg') != 'RS256' or not (key := keys.get(head.get('kid'))):
    sys.exit('Unknown key')
n, e = (int.from_bytes(b64url_decode(key[name])) for name in ('n', 'e'))
if not Pyjo.GCP.RSA.verify(n, e, f'{header}.{payload}'.encode(), b64url_decode(signature)):
    sys.exit('Invalid signature')
if claims['aud'] != audience or claims['exp'] < time.time():
    sys.exit('Not for this audience, or expired')

print(f'Valid token of {claims.get("email") or claims["sub"]} until {time.ctime(claims["exp"])}')
