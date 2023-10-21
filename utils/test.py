from web3 import Web3

function_signature = "getFeeBalance(address)"
hash = Web3.keccak(text=function_signature)
function_selector = hash.hex()[0:10]  # first 4 bytes

print(function_selector)