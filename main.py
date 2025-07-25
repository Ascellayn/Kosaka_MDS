# Kosaka Media Downloading Service (c) Ascellayn (2025) - TSN License 1.0 - Base
from KMDS.Globals import *;
from KMDS.API import API;

if (__name__ == '__main__'):
	Log.Clear(); TSN_Abstracter.Require_Version((3,0,0));
	Config.Logger.Print_Level = 15 if (Debug_Mode) else 20;
	Config.Logger.File = True;
	
	Log.Stateless(f"Kosaka Media Downloading Service (KMDS) {KMDS_Version}");
	API.run(Root_CFG["WebServer"]["Host"], Root_CFG["WebServer"]["Port"], Debug_Mode, use_reloader=False);