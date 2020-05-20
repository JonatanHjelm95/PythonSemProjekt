from flask import Flask, request
import VisualizeData as vd

app = Flask(__name__)
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

@app.route('/api/predict', methods = ['POST'])
def postJsonHandler():
    content = request.get_json()
    return vd.create_graph(name=str(content['name']), _type=str(content['type']))

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

