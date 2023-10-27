# Synapse Treasury 

This is a community run repository that helps to track the total amount of assets the the Synapse DAO Holds.

To run this project, clone the repository and run the following. Before beginning, you will need to fill out your own .env file with RPC nodes for all of the supported chains.

```
source venv/bin/activate
```

```
pip install -r requirements
```
```
python3 main.py
```
The file structure is as follows:

```
project/
│
├── main.py  
└── config/
    └── config.py
    └── timeData.py
└── data/
    └── currentTreasuryHoldings.csv
    └── treasurySums.csv
    └── treasuryHoldings_1_2023.csv
    └── treasurySums_1_2023.csv
└── Old/
    └── contractABI.json
    └── oldConfig.py
└── utils/
    └── test.py
    └── timestamps.py
```

# Methodology:

To aggregate all Synapse Treasury Holdings, two primary sets of contracts need to be tracked.
<br>
<br>
`claimed-fees`: Assets currently held in Synapse Treasury Wallets
<br>
`unclaimed-fees`: Fees that the protocol has accrued but hasnt been claimed from bridge contracts
<br>

Claimed fees can be tracked by directly getting the balance of all tokens the Treasury Wallet holds using RPC requests. Once this raw balance is returned we correct for decimals and multiply by the price at that timestamp as returned by Defillama's price API

Unclaimed fees are similar in that we can make an RPC call to the bridge, and read the `getFeeBalance` method which returns us the balance of tokens that are accrued fees. We then adjust decimals and multiply by the Defillama price. 

In the data folder, the script with the logic above is run and returned two types of summaries for each month. A "Sum" and a "Breakdown" - which is a more nuanced sum and tracks individual token balances.

All relevant contracts are open source and can be found in the [Synapse Main Repository](https://github.com/synapsecns/synapse-contracts) repository, as well as the [config](https://github.com/Defi-Moses/synapse-treasury/blob/main/config/config.py).

<br>
**IMPORTANT:** The current implementation doesnt track unclaimed assets in the Synapse Swap pools. This version is also missing Base Chain fees. 
<br>
<br>

Updates to come:
- Current Data fetch is currently buggy
- Possibly a fetch method to get the latest cached data (?)
- Code Clean up 
- Better testing / Testing suite
- Turn into a cli for better usability

Notes: 
- Relies on the Defillama pricing API for all prices

