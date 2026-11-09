# The ARN of the identity of the default profile of ~/.aws, or of AWS_PROFILE, as aws sts get-caller-identity
python -m Pyjo 'import Pyjo.AWS.Client as aws, Pyjo.AWS.Protocol.Query as q
print(aws.new(service="sts").call(q.new("GetCallerIdentity", version="2011-06-15")).at("Arn").text)'

# The account of a profile of the argument, of its SSO, aws login, role or credential_process
python -m Pyjo 'import Pyjo.AWS.Client as aws, Pyjo.AWS.Config as cfg, Pyjo.AWS.Protocol.Query as q
sts = aws.new(service="sts", config=cfg.new(profile=sys.argv[1]))
print(sts.call(q.new("GetCallerIdentity", version="2011-06-15")).at("Account").text)' dev

# The identity as the JSON of the AWS CLI, of the elements of the result of the XML of STS
python -m Pyjo 'import Pyjo.AWS.Client as aws, Pyjo.AWS.Protocol.Query as q
dom = aws.new(service="sts").call(q.new("GetCallerIdentity", version="2011-06-15"))
s(j({e.tag: e.text for e in dom.find("GetCallerIdentityResult > *")}), "\n")'
