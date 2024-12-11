from flask import Flask

app = Flask(__name__)


@app.route('/api/hello')
def hello():
    res = {"name":'myname','age':123,'obj':{'id':13421,'idx':12}}
    return res

if __name__ == '__main__':
    app.run(debug=True,port=12344)