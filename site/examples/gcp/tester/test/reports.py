import Pyjo.GCP.Call

from Pyjo.Util import url_escape


# The newest report of a prefix of a bucket of Cloud Storage, of the ones that a job writes each day, or None
def latest(storage, bucket, prefix):
    query = {'prefix': prefix, 'fields': 'items(name,updated)'}
    objects = storage.call(Pyjo.GCP.Call.new('GET', f'/storage/v1/b/{url_escape(bucket)}/o', query=query))
    items = objects.get('items', [])
    return max(items, key=lambda item: item['updated'])['name'] if items else None
