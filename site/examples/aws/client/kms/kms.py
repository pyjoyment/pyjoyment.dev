import Pyjo.AWS.Client
import Pyjo.AWS.Error
import Pyjo.AWS.Protocol.JSON

from Pyjo.Util import b64_decode, b64_encode

import sys


# The region and the credentials that the AWS CLI finds, of the environment or of a profile
kms = Pyjo.AWS.Client.new(service='kms')

# The encryption context, which authenticates the ciphertext, and which its decryption needs again
context = {'app': 'myapp'}


def encrypt(key_id, text):
    params = {'KeyId': key_id, 'Plaintext': b64_encode(text.encode(), ''), 'EncryptionContext': context}
    return kms.call(Pyjo.AWS.Protocol.JSON.new('TrentService.Encrypt', params))['CiphertextBlob']


# The ciphertext of a symmetric key names its key, so that its decryption needs no KeyId
def decrypt(ciphertext):
    params = {'CiphertextBlob': ciphertext, 'EncryptionContext': context}
    return b64_decode(kms.call(Pyjo.AWS.Protocol.JSON.new('TrentService.Decrypt', params))['Plaintext']).decode()


if len(sys.argv) != 3:
    sys.exit('Usage: kms.py KEY_ID TEXT')

ciphertext = encrypt(sys.argv[1], sys.argv[2])
print(f'Encrypted: {ciphertext}')
print(f'Decrypted: {decrypt(ciphertext)}')

try:
    decrypt(b64_encode(b'Not encrypted', ''))
except Pyjo.AWS.Error.object as e:
    print(f'Not decrypted: {e.code}')
