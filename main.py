# YT-DLP Server (c) Ascellayn (2025) = TSN License 1.0 - Base =
from YTDLPS.Globals import *;
from YTDLPS.API import API;

if (__name__ == '__main__'):
	Config.Logging["Print_Level"] = 20;
	Config.Logging["File"] = True;
	Log.Delete();
	TSN_Abstracter.Require_Version((2,0,0));
	Log.Info(f"YT-DLP Server {YTDLPS_Version}");

	API.run(Root_CFG["WebServer"]["Host"], Root_CFG["WebServer"]["Port"], True, use_reloader=False);