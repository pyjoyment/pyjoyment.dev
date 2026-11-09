# GET, and the title of the page
python -m Pyjo 'g("https://pyjoyment.dev").dom().at("title").text'

# POST of a form, and the JSON of the response
python -m Pyjo 'p("https://httpbin.org/post", form={"name": "Sara"}).json()["form"]'

# POST of JSON, and a value of the response by its JSON Pointer
python -m Pyjo 'p("https://httpbin.org/post", json={"name": "Sara"}).json("/json/name")'
