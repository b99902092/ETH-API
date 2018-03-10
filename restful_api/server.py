from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import json
import http.client

app = Flask(__name__)
api = Api(app)

class NodeInfo(Resource):
    def get(self):
        params = {'method': "admin_nodeInfo", "id":67}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection("127.0.0.1:8545")
        conn.request("POST", "/", json_params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        json_dict = json.loads(data.decode("utf-8"))
        result_dict = {}
        result_dict['enode'] = json_dict['result']['enode']
        result_dict['name'] = json_dict['result']['name']
        return jsonify(result_dict)

class BlockInfo(Resource):
    def get(self, block_number):
        params = {'method': "eth_getBlockByNumber", "params":[hex(int(block_number)), True], "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection("127.0.0.1:8545")
        conn.request("POST", "/", json_params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        json_dict = json.loads(data.decode("utf-8"))
        result_dict = {}
        result_dict['difficulty'] = int(json_dict['result']['difficulty'], 16)
        result_dict['gasLimit'] = int(json_dict['result']['gasLimit'], 16)
        result_dict['gasUsed'] = int(json_dict['result']['gasUsed'], 16)
        result_dict['hash'] = json_dict['result']['hash']
        result_dict['miner'] = json_dict['result']['miner']
        result_dict['parentHash'] = json_dict['result']['parentHash']
        result_dict['totalDifficulty'] = int(json_dict['result']['totalDifficulty'], 16)
        return jsonify(result_dict)

class TransactionInfo(Resource):
    def get(self, transaction_hash):
        params = {'method': "eth_getTransactionByHash", "params":[transaction_hash], "id":1}
        json_params = json.dumps(params)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection("127.0.0.1:8545")
        conn.request("POST", "/", json_params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        json_dict = json.loads(data.decode("utf-8"))
        result_dict = {}
        result_dict['blockHash'] = json_dict['result']['blockHash']
        result_dict['blockNumber'] = int(json_dict['result']['blockNumber'], 16)
        result_dict['from'] = json_dict['result']['from']
        result_dict['gas'] = int(json_dict['result']['gas'], 16)
        result_dict['gasPrice'] = int(json_dict['result']['gasPrice'], 16)
        result_dict['hash'] = json_dict['result']['hash']
        result_dict['nonce'] = int(json_dict['result']['nonce'], 16)
        result_dict['to'] = json_dict['result']['to']
        result_dict['value'] = int(json_dict['result']['value'], 16)
        return jsonify(result_dict)
        

api.add_resource(NodeInfo, '/node') # Route_1
api.add_resource(BlockInfo, '/block/<block_number>') # Route_2
api.add_resource(TransactionInfo, '/transaction/<transaction_hash>') # Route_3


if __name__ == '__main__':
     app.run(port=5002)