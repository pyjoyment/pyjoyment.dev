# A server on http://127.0.0.1:3000, as on any machine
python app.py daemon

# The ZIP of the function, without Pyjoyment, which the public layer of Pyjoyment gives the function
python app.py generate lambda-zip --arch arm64 --runtime python3.15 --function-only

aws lambda update-function-code --function-name hello --zip-file fileb://dist/function.zip
