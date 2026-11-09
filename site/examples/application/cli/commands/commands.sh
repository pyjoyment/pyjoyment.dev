# The commands of the application, of the script or of python -m MyApp
python app.py daemon -l 'http://*:8080'   # HTTP and WebSocket server
python app.py prefork -w 4                # four workers in processes of their own
python app.py routes -v                   # the routes, their names and methods

# A request without a server, with the CSS selector of the response
python app.py get /
python app.py get -v -M POST -c '{"name": "Pen", "price": 1.5}' /items
python app.py get / 'title' text

# Code against the application
python app.py eval -v 'app.home'
python app.py version

# Templates of __DATA__ into templates/, as the script grows
python app.py inflate
