@echo off
SET working_dir=%1

"..\SentinelUnrealTool.exe" -output_folder="%working_dir%" -b -store_build
"..\SentinelUnrealTool.exe" -output_folder="%working_dir%" -package_info
"..\SentinelReportsTool.exe" -output_folder="%working_dir%" -parse_raw
"..\SentinelClientTestTool.exe" -output_folder="%working_dir%" -run_tests
"..\SentinelReportsTool.exe" -output_folder="%working_dir%" -reports
