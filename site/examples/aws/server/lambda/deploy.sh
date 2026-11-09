# A server on http://127.0.0.1:3000, with the credentials of ~/.aws, as on any machine
uv run app.py daemon

# The ZIP of the function, without Pyjoyment and Pyjo-AWS, which tells the version of Pyjoyment of its layer
uv run app.py generate lambda-zip --arch arm64 --runtime python3.15 --function-only

# The public layer of that Pyjoyment, of the runtime and the region of the function
LAYERS=https://github.com/pyjoyment/Pyjoyment-Lambda-Layers/releases/latest/download/layers.json
LAYER=$(uv run --with Pyjoyment python -m Pyjo "g('$LAYERS').json('/pyjoyment-0_3_0-python3_15/eu-central-1')")

aws lambda create-function --function-name notes --runtime python3.15 --architectures arm64 \
  --handler app.handler --zip-file fileb://dist/function.zip --layers "$LAYER" \
  --role arn:aws:iam::123456789012:role/notes --environment 'Variables={TABLE=notes}'
aws lambda create-function-url-config --function-name notes --auth-type AWS_IAM
