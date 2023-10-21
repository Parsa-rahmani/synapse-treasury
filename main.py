import json
import requests
import csv
from web3 import Web3
from config import chains, tokens_by_chain


def make_rpc_request(url, method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        # This needs 
        "id": 1
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"RPC request failed with status code: {response.status_code}")
    
def get_balance(chain_name, msig_address, token_address, decimals):
    # Get the RPC URL from the chains dictionary
    url = chains[chain_name]['url']

    # Define the method and params
    data = "0x70a08231" + msig_address[2:].zfill(64)
    method = "eth_call"
    params = [{
        "to": token_address,
        "data": data  # balanceOf method signature + address without '0x'
    }, "latest"]

    # Make the RPC request
    response = make_rpc_request(url, method, params)

    # Extract the balance from the response
    balance_hex = response["result"]  # balance in hex
    if balance_hex == '0x':
        balance = 0
    else:
        balance = int(balance_hex, 16)  # convert from hex to decimal
    # Adjust for token decimals
    balance /= 10 ** decimals

    return balance

def get_fee_balance(chain_name, bridge_address, token_address, decimals):
    # Get the RPC URL from the chains dictionary
    url = chains[chain_name]['url']

    # Define the method and params
    # Function signature hash for getFeeBalance(address) is "0x4e71d92d"
    data = "0xc78f6803" + token_address[2:].zfill(64)
    method = "eth_call"
    params = [{
        "to": bridge_address,
        "data": data
    }, "latest"]

    # Make the RPC request
    response = make_rpc_request(url, method, params)

    # Extract the balance from the response
    balance_hex = response["result"]  # balance in hex
    if balance_hex == '0x':
        balance = 0
    else:
        balance = int(balance_hex, 16)  # convert from hex to decimal

    balance /= 10 ** decimals

    return balance

def get_defillama_price(chain_name, token_address):
    # Define the URL
    url = f"https://coins.llama.fi/prices/current/{chain_name}:{token_address}?searchWidth=4h"

    # Make the GET request
    response = requests.get(url)

    # Check the status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the price
        price = data['coins'][f'{chain_name}:{token_address}']['price']
        return price
    else:
        raise Exception(f"DeFiLlama API request failed with status code: {response.status_code}")
    

# First thing is to call get_balance of each of these tokens on the multisig and then run it through the DL price API 
def get_token_balances_and_values():
    # Initialize a dictionary to store the sums
    sums = {}

    with open('currentTreasuryHoldings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(["Chain", "Token Symbol", "Value", "Type"])

        # 1. Iterate over each chain in the chains dictionary
        for chain_name, chain_data in chains.items():
            # Initialize the sums for this chain
            sums[chain_name] = {"Claimed Fees": 0, "Unclaimed Fees": 0}

            # 2. For each chain, iterate over the tokens supported by that chain
            for token in tokens_by_chain.get(chain_name, []):
                # 3. Call the getBalance method on the multisig contract for each token
                balance = get_balance(chain_name, chain_data['multisig'], token[1], token[2])
                # Call the getFeeBalance method on the bridge contract for each token
                fee_balance = get_fee_balance(chain_name, chain_data['bridge'], token[1], token[2])
                # 4. Call the DeFiLlama API to get the price of the token
                price = get_defillama_price(chain_name, token[1])
                # 5. Multiply the balance by the price to get the value
                claimed_value = balance * price
                unclaimed_value = fee_balance * price

                # Add the values to the sums
                sums[chain_name]["Claimed Fees"] += claimed_value
                sums[chain_name]["Unclaimed Fees"] += unclaimed_value

                # 6. Store the chain, token address, token symbol, balance, and value
                writer.writerow([chain_name, token[0], claimed_value, "Claimed Fees"])
                writer.writerow([chain_name, token[0], unclaimed_value, "Unclaimed Fees"])

    # Write the sums to a new CSV file
    with open('sums.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(["Chain", "Claimed Fees", "Unclaimed Fees"])
        # Write the sums
        for chain_name, values in sums.items():
            writer.writerow([chain_name, values["Claimed Fees"], values["Unclaimed Fees"]])

#claimed, unclaimed, and total 

if __name__ == "__main__":
    get_token_balances_and_values()