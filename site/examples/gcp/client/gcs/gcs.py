import Pyjo.File
import Pyjo.GCP.Call
import Pyjo.GCP.Client
import Pyjo.GCP.Error

from Pyjo.Util import url_escape

import mimetypes
import sys


# The media upload of the JSON API, whose body is the content of the file, not JSON
class Upload(Pyjo.GCP.Call.object):
    def __init__(self, root, name, content):
        super().__init__('POST', f'/upload{root}/o', query={'uploadType': 'media', 'name': name})
        self.content = content
        self.content_type = mimetypes.guess_type(name)[0] or 'application/octet-stream'

    def build_tx(self, ua, url):
        url = Pyjo.GCP.Call.url_for(url, self.path, self.query)
        return ua.build_tx(self.method, url, {**self.headers, 'Content-Type': self.content_type}, self.content)


# The content of an object as it is, also of JSON, which a call would decode
class Download(Pyjo.GCP.Call.object):
    def parse(self, tx):
        return tx.res.body


# python gcs.py ls BUCKET [PREFIX] | put BUCKET NAME FILE | cat BUCKET NAME | rm BUCKET NAME
command, bucket, *args = sys.argv[1:]
root = '/storage/v1/b/' + url_escape(bucket)
storage = Pyjo.GCP.Client.new(service='storage')

try:
    if command == 'ls':
        query = {'prefix': args[0] if args else None, 'fields': 'items(name,size),nextPageToken'}
        while True:
            page = storage.call(Pyjo.GCP.Call.new('GET', root + '/o', query=query))
            for item in page.get('items', []):
                print(f'{item["size"]:>10} {item["name"]}')
            if not (token := page.get('nextPageToken')):
                break
            query['pageToken'] = token
    elif command == 'put':
        result = storage.call(Upload(root, args[0], Pyjo.File.path(args[1]).slurp()))
        print(f'{result["name"]}: {result["size"]} bytes of {result["contentType"]}')
    elif command == 'cat':
        # The name of an object is one segment of the path, with its slashes percent-encoded
        call = Download('GET', f'{root}/o/{url_escape(args[0])}', query={'alt': 'media'})
        sys.stdout.buffer.write(storage.call(call))
    elif command == 'rm':
        storage.call(Pyjo.GCP.Call.new('DELETE', f'{root}/o/{url_escape(args[0])}'))
except Pyjo.GCP.Error.object as e:
    sys.exit(e.message)
