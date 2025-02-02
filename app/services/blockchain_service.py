from web3 import Web3
import json
from app.config import settings

# Load contract details
CONTRACT_ADDRESS = "0xYourContractAddress"  # Replace with deployed contract address
ABI_PATH = "app/contracts/escrow.json"  # Path to ABI file

with open(ABI_PATH, "r") as file:
    CONTRACT_ABI = json.load(file)

# Connect to Ethereum network
web3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def lock_funds(buyer_private_key, seller_address, amount, release_time):
    buyer_account = web3.eth.account.privateKeyToAccount(buyer_private_key)
    txn = contract.functions.lockFunds(seller_address, release_time).buildTransaction({
        "from": buyer_account.address,
        "value": web3.toWei(amount, "ether"),
        "gas": 3000000,
        "nonce": web3.eth.getTransactionCount(buyer_account.address),
    })
    signed_txn = web3.eth.account.signTransaction(txn, buyer_private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_hash)

def release_funds(buyer_private_key, transaction_id):
    buyer_account = web3.eth.account.privateKeyToAccount(buyer_private_key)
    txn = contract.functions.releaseFunds(transaction_id).buildTransaction({
        "from": buyer_account.address,
        "gas": 3000000,
        "nonce": web3.eth.getTransactionCount(buyer_account.address),
    })
    signed_txn = web3.eth.account.signTransaction(txn, buyer_private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_hash)

def raise_dispute(buyer_private_key, transaction_id):
    buyer_account = web3.eth.account.privateKeyToAccount(buyer_private_key)
    txn = contract.functions.raiseDispute(transaction_id).buildTransaction({
        "from": buyer_account.address,
        "gas": 3000000,
        "nonce": web3.eth.getTransactionCount(buyer_account.address),
    })
    signed_txn = web3.eth.account.signTransaction(txn, buyer_private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_hash)
