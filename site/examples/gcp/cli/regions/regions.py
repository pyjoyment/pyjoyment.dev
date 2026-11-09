import Pyjo.GCP.Call
import Pyjo.GCP.Client
import Pyjo.GetOpt

from Pyjo.Util import url_escape

import sys


USAGE = """Usage: python regions.py [OPTIONS]

  python regions.py
  python regions.py --project myproject --zones
  python regions.py --status UP

Options:
  -h, --help              Show this summary of available options
  -p, --project <id>      Project, defaults to the one of the credentials
  -s, --status <status>   Only the regions of a status, UP or DOWN
  -z, --zones             Show the zones of each region
"""

getopt = Pyjo.GetOpt.new()
getopt.option('h|help').option('p|project=s').option('s|status=s', choices=['UP', 'DOWN']).option('z|zones')
if not (opts := getopt.parse()) or opts.help:
    sys.exit(USAGE)

compute = Pyjo.GCP.Client.new(service='compute', scopes=['https://www.googleapis.com/auth/compute.readonly'])

# The project of GOOGLE_CLOUD_PROJECT, of the key of a service account, of gcloud config set project for the user of
# gcloud auth application-default login, or of the metadata server
credentials = compute.credentials.credentials()
project = opts.project or (credentials and credentials.project) or sys.exit('No project: --project')

# The pages of the list, of nextPageToken
query = {'fields': 'items(name,status,zones),nextPageToken'}
while True:
    page = compute.call(Pyjo.GCP.Call.new('GET', f'/compute/v1/projects/{url_escape(project)}/regions', query=query))
    for region in page.get('items', []):
        if opts.status in (None, region['status']):
            zones = ' '.join(zone.rsplit('/', 1)[-1] for zone in region['zones']) if opts.zones else ''
            print(f'{region["name"]:<28}{region["status"]:<6}{zones}'.rstrip())
    if not (token := page.get('nextPageToken')):
        break
    query['pageToken'] = token
