# synapse-treasury


This is a repository that helps to track the total amount of assets the the Synapse DAO Holds. 

To run this project, clone the repository and run the following. Before beginning, you will need to fill out your own .env file with RPC nodes for all of the supported chains. 

source venv/bin/activate

pip install -r requirements

python3 main.py




The file structure is as follows:


project/
│
├── main.py
│
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



Updates to come: 
- Filter the script by chain 
- Code refactoring to allow both real time and historical data. 
- Possibly a fetch method to get the latest cached data


Feel free to contribute
