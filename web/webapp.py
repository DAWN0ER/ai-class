from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello():
    res = {"name":'myname','age':123,'obj':{'id':13421,'idx':12}}
    return res

@app.route('/id')
def idx():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=12344)