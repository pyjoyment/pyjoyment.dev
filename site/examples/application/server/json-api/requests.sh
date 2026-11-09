python app.py daemon &

curl http://127.0.0.1:3000/items
# [{"id":1,"name":"Pen","price":1.5}]

curl -d '{"name": "Notebook", "price": 4}' http://127.0.0.1:3000/items
# {"id":2,"name":"Notebook","price":4}

curl -d '{"name": "Notebook", "price": "cheap"}' http://127.0.0.1:3000/items
# {"errors":["\/price: Expected number - got string."]}
