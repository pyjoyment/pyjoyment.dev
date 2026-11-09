python worker.py

curl -d '{"name": "one"}' http://127.0.0.1:3000/jobs
curl -d '{"name": "two"}' http://127.0.0.1:3000/jobs
sleep 1
curl http://127.0.0.1:3000/status   # {"queued":0,"done":["one","two"]}
