..\..\SentinelUnrealTool.exe -output_folder=unittest_output  -c
..\..\SentinelUnrealTool.exe -output_folder=unittest_output -b -store_build
..\..\SentinelUnrealTool.exe -output_folder=unittest_output -package_info
..\..\SentinelUnrealTool.exe -output_folder=unittest_output -parse_info
..\..\SentinelClientTestTool.exe -output_folder=unittest_output -run_tests
..\..\SentinelReportsTool.exe -output_folder=unittest_output -reports
pause