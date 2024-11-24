from web3 import Web3

# Connect to Local or Test Ethereum Node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Replace with your Ethereum node URL
assert w3.isConnected(), "Connection to Ethereum node failed!"

# Accounts and Gas Configuration
deployer_account = w3.eth.accounts[0]  # Use the first account from your Ethereum node
w3.eth.default_account = deployer_account

# Contract ABI and Bytecode
contract_abi = [
    {
        "inputs": [{"internalType": "string", "name": "_message", "type": "string"}],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "message",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "_newMessage", "type": "string"}],
        "name": "updateMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract_bytecode = (
    "6080604052348015600e575f80fd5b506101438061001c5f395ff3fe608060405234801561000f575f80fd5b5060043610610034575f3560e01c80632e64cec1146100385780636057361d14610056575b5f80fd5b610040610072565b60405161004d919061009b565b60405180910390f35b610070600480360381019061006b91906100e2565b61007a565b005b5f8054905090565b805f8190555050565b5f819050919050565b61009581610083565b82525050565b5f6020820190506100ae5f83018461008c565b92915050565b5f80fd5b6100c181610083565b81146100cb575f80fd5b50565b5f813590506100dc816100b8565b92915050565b5f602082840312156100f7576100f66100b4565b5b5f610104848285016100ce565b9150509291505056fea26469706673582212209a0dd35336aff1eb3eeb11db76aa60a1427a12c1b92f945ea8c8d1dfa337cf2264736f6c634300081a0033"
)

# Deploy Contract
SimpleContract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
tx_hash = SimpleContract.constructor("Hello, Blockchain!").transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")

# Interact with the Contract
simple_contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

# Read Initial Message
initial_message = simple_contract_instance.functions.message().call()
print(f"Initial Message: {initial_message}")

# Update Message
tx_hash = simple_contract_instance.functions.updateMessage("Updated Message!").transact()
w3.eth.wait_for_transaction_receipt(tx_hash)

# Read Updated Message
updated_message = simple_contract_instance.functions.message().call()
print(f"Updated Message: {updated_message}")