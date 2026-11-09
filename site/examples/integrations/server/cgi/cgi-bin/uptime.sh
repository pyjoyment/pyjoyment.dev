#!/bin/sh
# The headers, an empty line and the body, as a CGI program writes its response
printf 'Content-Type: text/plain\r\n\r\n'
uptime
