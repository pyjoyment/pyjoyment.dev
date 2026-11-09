import Pyjo.GCP.Call
import Pyjo.GCP.Client
import Pyjo.GCP.Error

from Pyjo.Util import b64_decode, b64_encode

import sys


# python kms.py encrypt|decrypt projects/myproject/locations/europe-west1/keyRings/myring/cryptoKeys/mykey < in > out
command, key = sys.argv[1:3]
kms = Pyjo.GCP.Client.new(service='cloudkms')

# Cloud KMS encrypts 64 KiB at most: a larger file is encrypted with a key of its own, which Cloud KMS encrypts
data = sys.stdin.buffer.read()

# The bytes go in Base64 in the JSON, both ways; the decryption finds the version of the key in the ciphertext, so
# that the key rotates without a change here
try:
    if command == 'encrypt':
        result = kms.call(Pyjo.GCP.Call.new('POST', f'/v1/{key}:encrypt', {'plaintext': b64_encode(data, '')}))
        sys.stdout.buffer.write(b64_decode(result['ciphertext']))
        print(f'Encrypted with {result["name"]}', file=sys.stderr)
    elif command == 'decrypt':
        result = kms.call(Pyjo.GCP.Call.new('POST', f'/v1/{key}:decrypt', {'ciphertext': b64_encode(data, '')}))
        sys.stdout.buffer.write(b64_decode(result['plaintext']))
except Pyjo.GCP.Error.object as e:
    sys.exit(e.message)
