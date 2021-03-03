# rotki-challenge
CLI App that allows to manipulate BTC and ETH addresses in different ways.


## Requirements

- Python3.7
- pipenv

## Steps

1. Python 3.7
2. Install pipenv for virtual environment and package management
3. (Optional) Conver from Pipfile to requirements.txt with 
`pipenv run pip freeze > requirements.txt`
4. Run `pipenv install` or `pip install requirements`
5. Start shell with `pipenv shell`
6. **Make sure to provide you Kraken API Keys in a file located at the root directory (same depth as main/)**
7. Run `python -m main.main` to start the interactive shell
8. Test the application


## Tests

Starting from previous step 5:
6. Run `pytest`. All scripted tests should pass.


## Results from retrieving from Kraken
The CLI App saves open ordes and trades as simple files in the main directory. The
application does not allow to enter the name of the file where orders/trades.


## Goals
- [x] Retrieve Bitcoin wallets balances
- [x] Retrieve Ethereum addresses balances
- [x] Retrieve Ethereum addresses token balances
- [ ] Scan and retrieve swaps on ethereum addresses 
- [ ] Retrieve for Ethereum addresses transactions
- [x] Retrieve balances from Kraken
- [x] Retrieve open orders from Kraken and save on disk
- [x] Retrieve trades from Kraken and save on disk
- [x] Use modern Python
- [x] It works
- [ ] Use of linters
- [x] Use of typing
- [x] Testing
- [x] Resilience and error handling



## Observations
- After typing myself every function and class I understood why one would use Typing packages.
- Testing of main application is missing.
