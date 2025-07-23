# Kosaka Media Downloading Server (c) Ascellayn (2025) - TSN License 1.1 - Base
from KMDS.Globals import *;
from KMDS.API import API;

if (__name__ == '__main__'):
	Log.Clear(); TSN_Abstracter.Require_Version((2,0,0));
	Config.Logging["Print_Level"] = 15 if (Debug_Mode) else 20;
	Config.Logging["File"] = True;
	
	Log.Info(f"Kosaka YT-DLP Server {KMDS_Version}");
	API.run(Root_CFG["WebServer"]["Host"], Root_CFG["WebServer"]["Port"], Debug_Mode, use_reloader=False);