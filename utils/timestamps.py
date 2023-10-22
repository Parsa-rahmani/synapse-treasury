import requests
import datetime

chains = {
    'arbitrum': 42161,
    'aurora': 1313161554,
    'avax': 43114,
    # 'base': 8453, 
    'boba': 288, 
    'bsc': 56,
    # Canto needs to be done manually DL API doesnt support it
    # 'canto': 7700,
    'cronos': 25,
    'dfk': 53935,
    'dogechain': 2000,
    'ethereum': 1,
    'fantom': 250,
    # 'harmony': 1666600000,
    # 'klaytn': 8217,
    'metis': 1088,
    'moonriver': 1285,
    'moonbeam': 1284,  
    'optimism': 10,  
    'polygon': 137,
}

# Define the base URL for the defillama API
base_url = "https://coins.llama.fi/block/"

# Define the start and end years
start_year = 2023
end_year = 2024

# Initialize an empty dictionary to store the timestamps
timestamps = {}

# Loop over the chains
for chain in chains:
    # Initialize an empty list to store the timestamps for this chain
    timestamps[chain] = []

    # Loop over the months in the specified range
    for year in range(start_year, end_year):
        # NOTE this loop only stores information for the first 10 months. 
        for month in range(1, 10):
            # Get the first day of the month
            first_day = datetime.date(year, month, 1)

            # Get the timestamp for the first day of the month
            timestamp = int(first_day.strftime("%s"))

            # Add the timestamp to the list for this chain
            timestamps[chain].append(timestamp)

print(timestamps)

# # Define a function to get the data from the defillama API
# def get_defillama_data(chain, timestamp):
#     # Construct the URL for the API request
#     url = f"{base_url}{chain}/{timestamp}"

#     # Send the API request and get the response
#     response = requests.get(url)

#     try:
#         # Return the response data
#         return response.json()['height']
#     except Exception:
#         return 0

# # Initialize an empty dictionary to store the defillama data
# defillama_data = {}

# # Loop over the chains
# for chain in chains:
#     # Initialize an empty list to store the defillama data for this chain
#     defillama_data[chain] = []

#     # Loop over the timestamps for this chain
#     for timestamp in timestamps[chain]:
#         # Get the defillama data for this chain at this timestamp
#         data = get_defillama_data(chain, timestamp)

#         # Add the data to the list for this chain
#         defillama_data[chain].append(data)

# # Return the defillama data
# print(defillama_data)
