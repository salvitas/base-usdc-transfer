from web3 import Web3
from abi import ERC20_ABI

def get_token_contract(w3, contract_address):
    return w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)

def get_token_balance(contract, address):
    decimals = contract.functions.decimals().call()
    raw_balance = contract.functions.balanceOf(address).call()
    return raw_balance / (10 ** decimals)

def check_eth_balance(w3, address, threshold=0.0002):
    balance = w3.eth.get_balance(address)
    return w3.from_wei(balance, 'ether') > threshold

def send_usdc(w3, account, contract, to_address, amount):
    decimals = contract.functions.decimals().call()
    value = int(amount * (10 ** decimals))
    nonce = w3.eth.get_transaction_count(account.address)
    txn = contract.functions.transfer(Web3.to_checksum_address(to_address), value).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 60000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()
