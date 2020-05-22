from flask import Flask, request
import VisualizeData as vd

app = Flask(__name__)
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

@app.route('/api/predict', methods = ['POST'])
def getPrediction():
    content = request.get_json()
    return vd.create_graph(name=str(content['name']), _type=str(content['type']))


@app.route('/api/predict/specific', methods = ['POST'])
def getPrediction_advanced():
    content = request.get_json()
    return vd.create_graph_specific(name=str(content['name']), _type=str(content['type']), method=str(content['method']), n=str(content['n']), gamma=str(content['gamma']), kernel=str(content['kernel']))

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

