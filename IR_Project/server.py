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


@app.route('/search', methods=['GET'])
def search():
    print('search')
    try:
        data = request.get_json(force=True)
        res = coreSys.search(data)
        return jsonify(res)  
    except:
        raise #TODO handle
        return jsonify(success=False)

@app.route('/searchWE', methods=['GET'])
def searchWE():
    try:
        data = request.get_json(force=True)
        res = coreSys.searchWE(data)
        return jsonify(res)
    except:
        return jsonify(success=False)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
