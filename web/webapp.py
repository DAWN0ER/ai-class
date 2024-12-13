from flask import Flask,request, jsonify
from flask_cors import CORS
import os,json,time

app = Flask(__name__)
CORS(app) 

@app.route('/api/hello')
def hello():
    res = {"name":'myname','age':123,'obj':{'id':13421,'idx':12}}
    return res

@app.route('/api/list')
def get_list():
    res = os.listdir('../logs/save-20241116-20241130')
    return res

@app.route('/api/get', methods=['GET'])
def get_scene():
    script = request.args.get('script', default='', type=str)
    order = request.args.get('order', default=1, type=int)
    if script == '':
        return jsonify({'error': 'Missing script parameter'}), 400
    
    # TODO mock data
    with open('mock.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    order = min(order,len(data))
    rsp = data[order-1]
    return jsonify(rsp)

if __name__ == '__main__':
    app.run(debug=True,port=12344)