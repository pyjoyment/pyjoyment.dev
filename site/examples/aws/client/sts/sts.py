import Pyjo.AWS.Client
import Pyjo.AWS.Credentials
import Pyjo.AWS.Credentials.Static
import Pyjo.AWS.Protocol.Query

import sys


def call(action, **params):
    return Pyjo.AWS.Protocol.Query.new(action, params, version='2011-06-15')


# The region and the credentials that the AWS CLI finds, of the environment or of a profile
sts = Pyjo.AWS.Client.new(service='sts')

dom = sts.call(call('GetCallerIdentity'))
print(f'{dom.at("Account").text} {dom.at("Arn").text}')

# A role of the argument, whose temporary credentials sign the next calls
if len(sys.argv) > 1:
    dom = sts.call(call('AssumeRole', RoleArn=sys.argv[1], RoleSessionName='sts-py', DurationSeconds=900))
    credentials = Pyjo.AWS.Credentials.new(
        access_key_id=dom.at('AccessKeyId').text,
        secret_access_key=dom.at('SecretAccessKey').text,
        session_token=dom.at('SessionToken').text,
    )
    role = Pyjo.AWS.Client.new(service='sts', credentials=Pyjo.AWS.Credentials.Static.new(credentials))
    print(role.call(call('GetCallerIdentity')).at('Arn').text, 'until', dom.at('Expiration').text)
