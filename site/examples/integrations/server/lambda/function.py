import json


# An event function of AWS Lambda behind a REST API of API Gateway, as it runs there already, without Pyjoyment
def handler(event, context):
    name = (event.get('queryStringParameters') or {}).get('name', 'World')
    body = {'hello': name, 'path': event['path'], 'request': context.aws_request_id}
    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(body)}
