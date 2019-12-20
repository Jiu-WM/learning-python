import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import CT_ADP_NextItem
import CT_ADP_initializeSession


app = Flask(__name__)

@app.route('/adp/initializeSession/' , methods=['GET', 'POST'])
def initializeSession():
    CT_ADP_initializeSession.initialize()
    return json.dumps(CT_ADP_initializeSession.error)

@app.route('/adp/newitem/' , methods=['GET', 'POST'])
def nextitem():
    CT_ADP_NextItem.NextItem()
    return json.dumps(CT_ADP_NextItem.error)
    
     

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    # app.run(host='0.0.0.0',debug=True,port=4999)