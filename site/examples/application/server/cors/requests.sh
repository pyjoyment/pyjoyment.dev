python app.py daemon &

# The preflight of a request with JSON, answered before the routes
curl -i -X OPTIONS http://127.0.0.1:3000/api/user \
  -H 'Origin: https://app.example.com' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
# HTTP/1.1 204 No Content
# Access-Control-Allow-Credentials: true
# Access-Control-Allow-Headers: content-type
# Access-Control-Allow-Methods: GET, HEAD, POST, PUT, PATCH, DELETE
# Access-Control-Allow-Origin: https://app.example.com
# Access-Control-Max-Age: 600
# Vary: Origin, Access-Control-Request-Headers

# The request itself, from the frontend
curl -i http://127.0.0.1:3000/api/user -H 'Origin: https://app.example.com'
# HTTP/1.1 200 OK
# Access-Control-Allow-Credentials: true
# Access-Control-Allow-Origin: https://app.example.com
# Vary: Origin
#
# {"name":null}

# Another origin, which AllowedHosts stops before CORS
curl -i http://127.0.0.1:3000/api/user -H 'Origin: https://evil.example'
# HTTP/1.1 403 Forbidden
