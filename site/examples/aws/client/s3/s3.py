import Pyjo.AWS.Client
import Pyjo.AWS.Error
import Pyjo.AWS.Protocol.RestXML
import Pyjo.File
import Pyjo.Promise

from Pyjo.Util import url_escape

import mimetypes
import sys


if len(sys.argv) < 3:
    sys.exit('Usage: s3.py BUCKET ls [PREFIX] | get KEY | put FILE...')
bucket, command, args = sys.argv[1], sys.argv[2], sys.argv[3:]

# The region and the credentials that the AWS CLI finds, of the environment or of a profile
s3 = Pyjo.AWS.Client.new(service='s3')
RestXML = Pyjo.AWS.Protocol.RestXML.new


# The path of a key, percent-encoded but its slashes, as S3 signs it
def path(key=''):
    return f'/{url_escape(bucket)}/' + url_escape(key, r'^A-Za-z0-9\-._~/')


# The body of an object as it is, where the call gives an object of XML as a Pyjo.DOM
class GetObject(Pyjo.AWS.Protocol.RestXML.object):
    def parse(self, tx):
        return tx.res.body


if command == 'ls':
    listing = s3.call(RestXML('GET', path(), query={'list-type': 2, 'prefix': args[0] if args else ''}))
    for item in listing.find('Contents'):
        print(f'{item.at("Size").text:>10} {item.at("Key").text}')

elif command == 'get':
    try:
        sys.stdout.buffer.write(s3.call(GetObject('GET', path(args[0]))))
    except Pyjo.AWS.Error.object as e:
        sys.exit(f'{e.code}: {args[0]}')

# The files at the same time, non-blocking, with the types of the content of their names
elif command == 'put':

    def put(file):
        content_type = mimetypes.guess_type(file.basename())[0] or 'application/octet-stream'
        return s3.call_p(RestXML('PUT', path(file.basename()), file.slurp(), headers={'Content-Type': content_type}))

    Pyjo.Promise.all(*(put(Pyjo.File.new(name)) for name in args)).then(
        lambda *results: print(f'Uploaded {len(results)} files to s3://{bucket}/'),
        lambda e: sys.stderr.write(f'Not uploaded: {e}'),
    ).wait()
