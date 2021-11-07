# Nanoservices

## What's a nanoservice?

It's like a microservice, but smaller (and therefore better).

## Why use nanoservices?

Cons | Pros
---|---
Requires a Docker installation and creates a new container for every single function you have in your code  | It's a nice buzzword you can use at the next engineering all-hands meeting
 Every function call is replaced by a network-dependent GET request with absolutely **ZERO** error handling to make up for that fact|
Massive speed reductions (At least 200% slower or your money back) | 
Doesn't allow the use of classes and global variables |
Absolutely no way of enforcing signature contracts between functions - just send a GET request and hope for the best | 



# Format

- General
  - There are only two acceptable top-level components: functions and imports
  - That means: no global variables, no classes, etc (you don't need them anyways)
- Functions
  - Both multi and single line functions are acceptable, but not lambdas
- Imports
  - Imports can take the forms of `import MODULE` or `from MODULE import FUNCTION` (no aliases allowed)

## Side note:
The parsing is done with regular expressions. Python isn't a regular language - like most programming languages, it's a context-free language. 

(ie. this barely works, shouldn't work, and will probably break)

![](https://media.geeksforgeeks.org/wp-content/uploads/chomsky.png)


# Example

We start with a really simple program:

```python
def format_name(name):
  return name.capitalize()

def main():
  return "Hello, " + format_name("example")
```

The program is parsed with regex (again, bad idea), and breaks it into separate functions. 
```python
def format_name(name):
  return name.capitalize()
```
```python
def main():
  return "Hello, " + format_name("example")
```


Then, each function is converted into a Flask server.

First, we import the dependencies we need for the server, and initialize the server:
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def format_name(name):
  return name.capitalize()
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def main():
  return "Hello, " + format_name("example")
```

Next, we set up a route - when someone sends a `GET` request to `/`, it calls our function

```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name(name):
  return name.capitalize()
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return "Hello, " + format_name("example")
```

Now, we replace the arguments. Since we're passing the function arguments inside the `GET` request, we'll have to load the arguments from the request

```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('args'))[0]
  return name.capitalize()
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return "Hello, " + format_name("example")
```

Now, the return value has to be converted to JSON 
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('args'))[0]
  return jsonify(name.capitalize())
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return jsonify("Hello, " + format_name("example"))
```

Then, it replaces each function call with a `GET` request.



```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('args'))[0]
  return jsonify(name.capitalize())
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return jsonify("Hello, " + requests.get(f'http://format_name:5000/?args=["example"]').json())
```

To break that down a little:
- http://format_name refers to a Docker container. Docker containers can query each other by their name, and we name each Docker container after its function
- The port queried is `5000`, because we run a Flask server in each container (which defaults to `5000`)
- The arguments list is a little messy:
  - Instead of refering to the arguments by name, it's easier to just have one argument: `args`
  - `args` is a list, which contains all of the actual arguments in the order they appear
  - So, `function(firstname, lastname)` would become `args=[{firstname}, {lastname}]`





Finally, we have to start the app
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('args'))[0]
  return jsonify(name.capitalize())

app.run(host='0.0.0.0')
```
```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return jsonify("Hello, " + requests.get(f'http://format_name:5000/?args=["example"]').json())

app.run(host='0.0.0.0')
```







  




Now: everything has been converted to standalone servers.

Next, we generate the `Dockerfile`s, which will build the Docker images. Then, a `docker-compose` file is created, which allows us to start all of these containers at once. 

