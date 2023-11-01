import json
import requests
import web3
import time
from web3 import Web3
from web3.exceptions import TimeExhausted


w3 = Web3(web3.HTTPProvider('https://rpc.builder0x69.io'))
w3_p = Web3(web3.HTTPProvider('https://rpc.pulsechain.com'))

contract_address = "0x98dFB360cbc65045a8415FA2514F549cD3000f02"
block_number = 18303690
api_key = ""
private_key = ""
sender_address = w3.eth.account.from_key(private_key).address

if w3.is_connected():
    print('ETH rpc链接成功')
else:
    print('ETH rpc链接失败')
if w3_p.is_connected():
    print('pls rpc链接成功')
else:
    print('pls rpc链接失败')

url = f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock={block_number}&apikey={api_key}"

response = requests.get(url)
data = json.loads(response.text)

transactions = data['result']
print(f'length:{len(transactions)}')

def send_tx(to, hex_data, gas_limit, gas_price, nonce):
    tx = {
        'to': to,
        'data': hex_data,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'value': 0,
        'chainId': 369
    }
    try:
        signed_tx = w3_p.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3_p.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3_p.eth.wait_for_transaction_receipt(tx_hash)
        print("已发送交易：", tx_hash.hex())
        while True:
            if tx_receipt is not None:
                print(f"交易成功：第{i}笔")
                break
    except TimeExhausted as e:
        print("错误", str(e))
        print("尝试取消交易")
        send_tx(sender_address, "0x", 833333, int(w3_p.eth.gas_price * 10), w3_p.eth.get_transaction_count(sender_address))
        print("已取消")

i = 0
n = w3_p.eth.get_transaction_count(sender_address)
for transaction in transactions:
    i += 1
    print(f"nounce为{w3_p.eth.get_transaction_count(sender_address)}")
    try:
        send_tx(contract_address, transaction["input"], 833333, int(w3_p.eth.gas_price * 1.3), w3_p.eth.get_transaction_count(sender_address))
    except:
        print("返回重试")
        break





