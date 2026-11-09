"""
Usage: regions.py [OPTIONS]

  python regions.py
  python regions.py --all --profile dev
  python regions.py --region us-east-1 --endpoints

Options:
  -a, --all              Also the regions that the account has not opted in to
  -e, --endpoints        Show the endpoints of EC2 of the regions
  -h, --help             Show this summary
  -p, --profile <name>   Profile of ~/.aws, instead of AWS_PROFILE
  -r, --region <name>    Region of the request, instead of the one of the profile
"""

import Pyjo.AWS.Client
import Pyjo.AWS.Config
import Pyjo.AWS.Protocol.Query

from Pyjo.Util import getopt

import sys


opts = getopt({'a|all': None, 'e|endpoints': None, 'h|help': None, 'p|profile=s': None, 'r|region=s': None})
if not opts or opts.help or len(sys.argv) > 1:
    sys.exit(__doc__.strip())

ec2 = Pyjo.AWS.Client.new(service='ec2', region=opts.region, config=Pyjo.AWS.Config.new(profile=opts.profile))
call = Pyjo.AWS.Protocol.Query.new('DescribeRegions', {'AllRegions': bool(opts.all)}, version='2016-11-15')

# The XML of EC2, whose names are in lower camel case, unlike the other APIs of the query protocol
for item in sorted(ec2.call(call).find('regionInfo > item'), key=lambda item: item.at('regionName').text):
    columns = [item.at('regionName').text]
    if opts.endpoints:
        columns.append(item.at('regionEndpoint').text)
    if opts.all:
        columns.append(item.at('optInStatus').text)
    print('\t'.join(columns))
