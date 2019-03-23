# Sentinel Project # 
The sentinel project is a container for all of the sentinel plugins that do the heavy lifting for the game automation. The traditional way of running the test environment is to clone the SentinelUE4 project which contains this project as a submodule.

[SentinelUE4 Repo](https://github.com/BusMoneyGames/SentinelUE4)

## Prerequisits ##
### Windows ###
- Python 3.6 + 
- Pipenv

### Running the Integration tests ###

The sentinel plugins in some cases don't do very interesting things when run in isolation so the primary responsibility of the Sentinel project is to be a container for the different plugins so we can run integration tests.

pipenv install --dev 
pipenv run TestRunner.py -h
pipenv run TestRunner.py -editor
