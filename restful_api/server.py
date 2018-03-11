from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import json
import http.client
from config import geth_addr

app = Flask(__name__)
api = Api(app)

class NodeInfo(Resource):
    def get(self):

        # invoke the admin_nodeInfo RPC
        params = {'method': "admin_nodeInfo", "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(geth_addr)
        try:
            conn.request("POST", "/", json_params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as error:
            result = {"error": "The service of Geth may be down.", "error_type": str(type(error))}
            return jsonify(result)

        # process the result of the admin_nodeInfo
        json_dict = json.loads(data.decode("utf-8"))
        result = {}
        result['enode'] = json_dict['result']['enode']
        result['name'] = json_dict['result']['name']
        return jsonify(result)

class BlockInfo(Resource):
    def get(self, block_number):
        
        # invoke the eth_getBlockByNumber RPC
        params = {'method': "eth_getBlockByNumber", "params":[hex(int(block_number)), True], "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(geth_addr)
        try:
            conn.request("POST", "/", json_params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as error:
            result = {"error": "The service of Geth may be down.", "error_type": str(type(error))}
            return jsonify(result)

        # process the result of the RPC
        try:
            json_dict = json.loads(data.decode("utf-8"))
            result = {}
            if 'result' in json_dict:
                # result is None => block is not found
                if json_dict['result'] == None:
                    result = {"message": "block is not found."}
                # normal result
                else:
                    result['difficulty'] = int(json_dict['result']['difficulty'], 16)
                    result['gasLimit'] = int(json_dict['result']['gasLimit'], 16)
                    result['gasUsed'] = int(json_dict['result']['gasUsed'], 16)
                    result['hash'] = json_dict['result']['hash']
                    result['miner'] = json_dict['result']['miner']
                    result['parentHash'] = json_dict['result']['parentHash']
                    result['totalDifficulty'] = int(json_dict['result']['totalDifficulty'], 16)
            # error exists in the result => put the error message into return result
            elif 'error' in json_dict:
                result = {'error':json_dict['error']}
        except Exception as error:
            result = {"error": "something wrong", "error_type": str(type(error))}

        return jsonify(result)

class TransactionInfo(Resource):
    def get(self, transaction_hash):

        # invoke the eth_getTransactionByHash RPC
        params = {'method': "eth_getTransactionByHash", "params":[transaction_hash], "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(geth_addr)
        try:
            conn.request("POST", "/", json_params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as error:
            result = {"error": "The service of Geth may be down.", "error_type": str(type(error))}
            return jsonify(result)
        
        # process the result of RPC
        try:
            json_dict = json.loads(data.decode("utf-8"))
            result = {}
            if "result" in json_dict:
                # the result is None => transaction is not found
                if json_dict['result'] == None:
                    result = {"message": "transaction is not found."}
                # normal result
                else:
                    result['blockHash'] = json_dict['result']['blockHash']
                    result['blockNumber'] = int(json_dict['result']['blockNumber'], 16)
                    result['from'] = json_dict['result']['from']
                    result['gas'] = int(json_dict['result']['gas'], 16)
                    result['gasPrice'] = int(json_dict['result']['gasPrice'], 16)
                    result['hash'] = json_dict['result']['hash']
                    result['nonce'] = int(json_dict['result']['nonce'], 16)
                    result['to'] = json_dict['result']['to']
                    result['value'] = int(json_dict['result']['value'], 16)
            # error exists in the result => put the error message into return result
            elif "error" in json_dict:
                result['error'] = json_dict['error']
        except Exception as error:
            result = {"error": "Something wrong.", "error_type": str(type(error))}
        
        return jsonify(result)

class Miner(Resource):
    def put(self):
        # invoke the miner_start RPC
        params = {'method': "miner_start", "params":[1], "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(geth_addr)
        try:
            conn.request("POST", "/", json_params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as error:
            result = {"error": "The service of Geth may be down.", "error_type": str(type(error))}
            return jsonify(result)

        # process the result of RPC
        json_dict = json.loads(data.decode("utf-8"))
        if 'result' in json_dict and json_dict['result'] == None:
            result = {"message": "start mining with 1 thread"}
        else:
            result = {"error": "something wrong"}

        return jsonify(result) 

    def delete(self):
        # invoke the miner_stop RPC
        params = {'method': "miner_stop", "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(geth_addr)
        try:
            conn.request("POST", "/", json_params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as error:
            result = {"error": "The service of Geth may be down.", "error_type": str(type(error))}
            return jsonify(result)

        json_dict = json.loads(data.decode("utf-8"))
        if 'result' in json_dict and json_dict['result'] == True:
            result = {"message": "stop mining succesfully"}
        else:
            result = {"error": "something wrong"}

        return jsonify(result)

api.add_resource(NodeInfo, '/node')
api.add_resource(BlockInfo, '/block/<block_number>')
api.add_resource(TransactionInfo, '/transaction/<transaction_hash>')
api.add_resource(Miner, '/mining')


if __name__ == '__main__':
     app.run(debug=True)