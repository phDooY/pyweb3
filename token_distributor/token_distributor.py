import csv
import json
import sys
from time import sleep
from eth_utils import from_wei
from web3 import Web3, IPCProvider

def cont():
    answer = raw_input('Continue? (y/n)\n')
    while not answer.lower() in ['y', 'n']:
        answer = raw_input('Continue? (y/n)\n')
    if answer.lower() == 'y':
        pass
    else:
        exit()

def unlock():
    global acct_passhrase
    while not web3.personal.unlockAccount(acct, acct_passhrase):
        print 'Wrong passphrase for account %s' % acct
        acct_passhrase = raw_input('Enter your accounts passhrase: ')
    print 'Account %s unlocked' % acct


def wrire_out_csv(data):
    csv_file_out = csv_file.split('.csv')[0] + '_out.csv'
    with open(csv_file_out, 'w') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


web3 = Web3(IPCProvider())

acct = raw_input('Enter your account: ')
#acct = '0x58DdB9b2D3D6dD0c14a8d78eF3017985B25De56A'

acct_passhrase = raw_input('Enter your passhrase: ')
#acct_passhrase = ''

unlock()

print "Web3 provider is", web3.providers[0]
print "Owner address is", acct
print "Owner balance is", from_wei(web3.eth.getBalance(acct), "ether"), "ETH"
print '\n'

csv_file = raw_input('\nPlace csv file in the same directory.\n'
                     'Enter file name: ')
#csv_file = 'file.csv'

contract_address = raw_input('Enter contract address: ')
#contract_address = '0x07acaEfF69B4c17c0E40f6af957D6971d66a8642' # insert your deployed contract address here

contract_abi_txt = raw_input('Enter contract JSON interface (ABI) in plain text: ')
#contract_abi_txt = '[ { "constant": true, "inputs": [], "name": "name", "outputs": [ { "name": "", "type": "string", "value": "Confido Token" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "approve", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "name": "", "type": "uint256", "value": "1.5e+25" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "INITIAL_SUPPLY", "outputs": [ { "name": "", "type": "uint256", "value": "1.5e+25" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "name": "", "type": "uint8", "value": "18" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_subtractedValue", "type": "uint256" } ], "name": "decreaseApproval", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "_owner", "type": "address" } ], "name": "balanceOf", "outputs": [ { "name": "balance", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "name": "", "type": "string", "value": "CFD" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name": "transfer", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type": "address" }, { "name": "_addedValue", "type": "uint256" } ], "name": "increaseApproval", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "_owner", "type": "address" }, { "name": "_spender", "type": "address" } ], "name": "allowance", "outputs": [ { "name": "remaining", "type": "uint256", "value": "0" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "owner", "type": "address" }, { "indexed": true, "name": "spender", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type": "address" }, { "indexed": true, "name": "to", "type": "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" } ]'

contract_abi = json.loads(contract_abi_txt)

contract = web3.eth.contract(contract_abi, contract_address)

with open(csv_file, "rt") as inp:
    reader = csv.DictReader(inp)
    rows = [row for row in reader]

for row in rows:
    transaction = {"from": acct, "gasPrice": int(web3.eth.gasPrice / 3), "gas": 40000}
    account_to = row['account']
    amount = row['amount']
    if amount == 0:
        continue

    passed = False
    while not passed:
        try:
            tx = contract.transact(transaction).transfer(account_to, int(amount)*10**18)
            passed = True
        except ValueError:
            print 'Unlocking account...'
            unlock()
        except MemoryError:
            print 'MemoryError. Waiting 15 sec...'
            sleep(15)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print 'Account: %s' % account_to
            print 'Amount: %s' % amount
            wrire_out_csv(rows)
            raise

    row.update({"tx": tx})

    print 'Account: %s' % account_to
    print 'Amount: %s' % amount
    print 'Tx: %s' % tx
    print '\n'

wrire_out_csv(rows)