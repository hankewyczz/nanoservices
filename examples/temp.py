import json
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/', methods=['GET'])
def generate_list():
    import random
    return jsonify(random.sample(range(1, 100), json.loads(request.args.get('args'))[0]))

app.run()