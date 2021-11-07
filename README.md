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

## Why?

I was bored

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

We import the dependencies we need for the server, and initialize the server:
```python
# I'll exclude the imports to make this simpler

app = Flask(__name__)

def format_name(name):
  return name.capitalize()
```
```python
app = Flask(__name__)

def main():
  return "Hello, " + format_name("example")
```

Next, we set up a route - when someone sends a `GET` request to `/`, it calls our function

```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name(name):
  return name.capitalize()
```
```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return "Hello, " + format_name("example")
```

Now, we handle function arguments for every function with arguments (in this case, only `format_name`).

Since we call the function via a request, we have to manually grab the arguments from the request, rather than directly from the function. 

```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('name'))
  return name.capitalize()
```
`json.loads()` takes a JSON string, and converts it to a Python object (allowing us to handle the argument as it was passed).

Now, the return value has to be converted to JSON 
```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('name'))
  return jsonify(name.capitalize())
```
```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return jsonify("Hello, " + format_name("example"))
```

Then, it replaces each function call with a `GET` request.



```python
format_name("example")
```
gets replaced by
```python
requests.get(f'http://format_name:5000/?name={json.dumps("example")}').json()
```

To break that down a little:
- `http://format_name` refers to a Docker container named `format_name`. Docker containers can call each other by their name, and we name each Docker container after its function
- We query port `5000`, because that's where the Flask server is running
- The arguments are parsed thru `json.dumps()`, which converts the argument to valid JSON
- Finally, we convert the response to JSON via the `.json()` call





Finally, we have to start the app
```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def format_name():
  name = json.loads(request.args.get('name'))
  return jsonify(name.capitalize())

app.run(host='0.0.0.0')
```
```python
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
  return jsonify("Hello, " + 
                requests.get(f'http://format_name:5000/?name={json.dumps("example")}').json())

app.run(host='0.0.0.0')
```







  




Now: everything has been converted to standalone servers.

Next, we generate the `Dockerfile`s, which will build the Docker images. Then, a `docker-compose` file is created, which allows us to start all of these containers at once. 

