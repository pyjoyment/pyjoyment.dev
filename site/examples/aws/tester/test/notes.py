import Pyjo.AWS.Client
import Pyjo.AWS.Error
import Pyjo.AWS.Protocol.RestXML

from Pyjo.Util import url_escape


# The characters of a key that its path keeps, as S3 signs the path as it is
KEEP = r'^A-Za-z0-9\-._~/'


# The notes of a bucket of S3, under a prefix, with the client of S3 that the application or its test gives
class Notes:
    def __init__(self, bucket, s3=None, prefix='notes/'):
        self.root = '/' + url_escape(bucket)
        self.s3 = s3 or Pyjo.AWS.Client.new(service='s3')
        self.prefix = prefix

    def path(self, name):
        return f'{self.root}/{url_escape(self.prefix + name, KEEP)}'

    def names(self):
        call = Pyjo.AWS.Protocol.RestXML.new('GET', self.root, query={'list-type': 2, 'prefix': self.prefix})
        return [key.text.removeprefix(self.prefix) for key in self.s3.call(call).find('Contents > Key')]

    def load(self, name):
        try:
            return self.s3.call(Pyjo.AWS.Protocol.RestXML.new('GET', self.path(name))).decode()
        except Pyjo.AWS.Error.object as e:
            if e.code == 'NoSuchKey':
                return None
            raise

    def save(self, name, text):
        headers = {'Content-Type': 'text/plain;charset=UTF-8'}
        self.s3.call(Pyjo.AWS.Protocol.RestXML.new('PUT', self.path(name), text.encode(), headers=headers))
