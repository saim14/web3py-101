from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()



with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# install_solc("0.6.0")
compiled_sol = compile_standard({
    "language" : "Solidity",
    "sources": {
        "SimpleStorage.sol": {
            "content": simple_storage_file
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": [
                    "abi", "metadata", "evm.bytecode", "evm.sourceMap"
                ]
            }
        }
    }
},
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get ABI 
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache / testnet
w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/53d9659c7d1640fd9353fe9e98f9c64a"))
chain_id = 42
my_address = "0x4F2743031D786C57CC2253ee40a4FeF74718abdD"
private_key = os.getenv("PRIVATE_KEY")

# Create the contact in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get lates transaction
nonce = w3.eth.getTransactionCount(my_address)

# Build a transaction
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price, 
    'chainId': chain_id,
    'from': my_address,
    'nonce': nonce,
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Working with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Initial value of favourite number
print("Initial value of favourite number")
print(simple_storage.functions.get().call())

store_transaction = simple_storage.functions.store(150).buildTransaction({
    "gasPrice": w3.eth.gas_price, 
    'chainId': chain_id,
    'from': my_address,
    'nonce': nonce + 1,
})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.waitForTransactionReceipt(send_store_txn)

print("After transaction value of favourite number")
print(simple_storage.functions.get().call())