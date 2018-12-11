# Sentinel Unreal Project # 
The sentinel UE4 project is the test project for the sentinel tool suit,  This project allows for testing sentinel in a simple environment built for running fast

The Sentine-UE4 project also contains the Sentinel Automation Unreal plugin code that allows the game client to be run in automation mode for client tests

## Prerequisites ##

- Unreal Engine 4.21 ( Can be installed through the epic games launcher )
- Visual Studio 2017 ( any version that it compatible with the Unreal version )
- Python 3.6 with pipenv
- Access to the sentinel project to clone the sub project

## Running sentinel / Creating the test environment ##

- Run make_exe.bat
- Edit sentinel_settings.json to make sure that the path to engine is set correctly
- Run "SentinelTool/bin/_tests/test_run_all.bat"
- This will take around 10 min since it runs the client tests
- Wait for the run to finish
- Go to the SentinelReports/Reports/index.html

