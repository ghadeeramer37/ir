from flask import Flask, request, jsonify
from importlib_metadata import method_cache
from modules.coreSystem import coreSys
port = 8000
app = Flask(__name__)


@app.route('/', methods=['GET'])
def initialize():
    print("initialize")
    try:
        coreSys.initialize()
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/search/<int:typeSearch>/<string:query>', methods=['GET'])
def search(typeSearch,query):
    print('search')
    try:
        if typeSearch==1:
            res = coreSys.search(query)
        else:
            res = coreSys.searchWE(query)
        #data = request.get_json(force=True)
        
        return jsonify(res)  
    except:
        raise #TODO handle



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
