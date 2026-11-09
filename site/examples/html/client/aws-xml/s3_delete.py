import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.RestXML
import Pyjo.Template

from Pyjo.Util import url_escape

import base64
import hashlib
import sys


# The XML of DeleteObjects, from a template that escapes the keys, as a & in a name of a file
DELETE = """<?xml version="1.0" encoding="UTF-8"?>
<Delete xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
% for key in keys:
  <Object><Key><%= key %></Key></Object>
% end
</Delete>
"""

bucket, prefix = sys.argv[1:3]
root = '/' + url_escape(bucket)

# The region and the credentials that the AWS CLI finds, of the environment or of a profile
s3 = Pyjo.AWS.Client.new(service='s3')

# The XML of a response, as a Pyjo.DOM object of XML, which CSS selectors query
listing = s3.call(Pyjo.AWS.Protocol.RestXML.new('GET', root, query={'list-type': 2, 'prefix': prefix}))
keys = listing.find('Contents > Key').map('text').to_list()
if not keys:
    sys.exit(f'Nothing under {prefix}')

xml = Pyjo.Template.new(vars=True, auto_escape=True).render(DELETE, {'keys': keys}).encode()
headers = {'Content-MD5': base64.b64encode(hashlib.md5(xml).digest()).decode(), 'Content-Type': 'application/xml'}
result = s3.call(Pyjo.AWS.Protocol.RestXML.new('POST', f'{root}?delete', xml, headers=headers))

for key in result.find('Deleted > Key').map('text'):
    print(f'Deleted {key}')
for error in result.find('Error'):
    print(f'Not deleted {error.at("Key").text}: {error.at("Message").text}')
