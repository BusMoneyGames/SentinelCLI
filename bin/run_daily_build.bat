%~dp0..\SentinelUnrealTool.exe -c
%~dp0..\SentinelUnrealTool.exe -rebuild_lighting
%~dp0..\SentinelUnrealTool.exe -package_info
%~dp0..\SentinelUnrealTool.exe -parse_info
%~dp0..\..\SentinelUnrealTool.exe -resave_blueprints
%~dp0..\SentinelUnrealTool.exe -b --store_build
%~dp0..\SentinelReportsTool.exe -reports
%~dp0..\SentinelUpload.exe -upload_reports
%~dp0..\SentinelMessaging.exe -build_notify
pause