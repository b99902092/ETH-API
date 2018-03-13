# Readme

## Support Functionality

### View Node Information
URL of api: localhost:5000/node  
HTTP method: GET

### View Block Information
URL of api: localhost:5000/block/{block_number}  
HTTP method: GET

### View Transaction Information
URL of api: localhost:5000/transaction/{transaction_hash}  
HTTP method: GET

### Start mining
URL of api: localhost:5000/mining  
HTTP method: PUT

### Stop mining
URL of api: localhost:5000/mining  
HTTP method: DELETE

### Send Transaction
URL of api: localhost:5000/transaction  
HTTP method: POST  
Parameters:
* from
* to (optional when creating new contract)
* gas (optional)
* gasPrice (optional)
* value (optional)
* data
* nonce (optional)

### Access Rate Limit
Default rate limit is 10 times per hour. You can modify the default rate limit in config.py.

## How to Run

### Geth
Go to the folder of geth and run the geth. Add the option --rpc to make geth listen the RPC via HTTP. Add the option --rpcapi admin,eth,minter to enable the admin, official DApp and miner API over the HTTP interface. Add the option --etherbase {your_hash_addr} to let miner know the addr. Thus, the cmd you issue to the cmd line may be 'geth.exe --rpcapi eth,admin,miner --rpc --etherbase "{your_hash_addr}"'

### Server
I use flask to implement these restful APIs. Thus, you may need to install some python packages at first. The following are the packages you may need: flask, flask-restful, flask_limiter. You can run the server through the cmd like this "python server.py". You can revise the ip and the port your geth node listened to in the config.py. Besides, you can also revise the default rate limit of apis in the config.py. You can refer to the flask_limiter package about how to adjust the default rate limit.

## Environment
This project is run on Windows 10.
The python version is 3.5.2.
The default URL and port the server listening to is "127.0.0.1:5000".


