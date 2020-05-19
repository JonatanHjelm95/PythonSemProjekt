from flask import Flask
from flask import request
import VisualizeData as vd
import os

app = Flask(__name__)


@app.route('/predict', methods = ['POST'])
def postJsonHandler():
    try:
        content = request.get_json()
        name = str(content['name'])
        _type = str(content['type'])
        return  vd.create_graph(name, _type)
    except Exception as e:
        return e
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

