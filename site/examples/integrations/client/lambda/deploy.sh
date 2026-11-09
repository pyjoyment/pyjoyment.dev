# The ZIP of app.py and wrapper.py, without Pyjoyment, which the public layer of Pyjoyment gives the function
python app.py generate lambda-zip --arch arm64 --runtime python3.15 --function-only

# A function of the runtime python3.15 with the layer, whose wrapper and Function URL stream, as the application is told
aws lambda update-function-code --function-name answer --zip-file fileb://dist/function.zip
aws lambda update-function-configuration --function-name answer --handler app.handler --environment 'Variables={
  AWS_LAMBDA_EXEC_WRAPPER=/var/task/wrapper.py,
  PYJO_LAMBDA_INVOKE_MODE=RESPONSE_STREAM,
  PYTHONPATH=/opt/python/lib/python3.15/site-packages
}'
aws lambda create-function-url-config --function-name answer --auth-type AWS_IAM --invoke-mode RESPONSE_STREAM

# The words as they come, a request signed with the credentials of the environment
curl -N --aws-sigv4 aws:amz:eu-central-1:lambda --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -H "X-Amz-Security-Token: $AWS_SESSION_TOKEN" https://<url-id>.lambda-url.eu-central-1.on.aws/answer
