python app.py daemon -p -l 'http://*:3000' &

# Behind a proxy of HTTPS, which -p trusts
curl -I -H 'X-Forwarded-Proto: https' http://127.0.0.1:3000/
# HTTP/1.1 200 OK
# Cache-Control: private
# Content-Security-Policy: base-uri 'self'; frame-ancestors 'self'; object-src 'none'; report-uri /csp-reports; report-to csp
# Content-Security-Policy-Report-Only: default-src 'self' 'nonce-vahmKSLVOvloaKjJjucfww=='; img-src 'self' data:; frame-ancestors 'none'; report-uri /csp-reports; report-to csp
# Cross-Origin-Opener-Policy: same-origin
# Permissions-Policy: camera=(), geolocation=(), microphone=(), fullscreen=(self)
# Referrer-Policy: strict-origin-when-cross-origin
# Reporting-Endpoints: csp="/csp-reports"
# Strict-Transport-Security: max-age=300
# X-Content-Type-Options: nosniff

# A report of a browser, as the image of another host would make
curl -i http://127.0.0.1:3000/csp-reports -H 'Content-Type: application/csp-report' \
  -d '{"csp-report": {"document-uri": "http://127.0.0.1:3000/", "effective-directive": "img-src", "blocked-uri": "https://tracker.example/pixel.gif", "disposition": "report"}}'
# HTTP/1.1 204 No Content
# [warn] CSP violation of img-src: https://tracker.example/pixel.gif in http://127.0.0.1:3000/ (report only)
# [info] img-src blocked https://tracker.example/pixel.gif
