from TSN_Abstracter import *;
import httpx, json, time;

Log.Clear();
TSN_Abstracter.Require_Version((3,0,0))
Config.Logger.Print_Level = 15;

Root_CFG: dict = File.JSON_Read("Root_CFG.json");
WebServer_URL: str = f"http://{Root_CFG['WebServer']['Host']}:{Root_CFG['WebServer']['Port']}";


def Request_Handler(URL: str) -> None:
	Log.Info(f"Fetching files for {URL}...")
	Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=json.dumps({"URL": URL}, indent=0), timeout=60);
	try:
		Request_JSON: dict = Request.json(); Log.Fetch_ALog().OK(); Log.Debug(str(Request_JSON));
		if (Request_JSON["Status"] != 200): Log.Fetch_ALog().ERROR(Request_JSON["Error"]); return;
		File.JSON_Write(f"Downloads/REQUEST_HANDLER.JSON", Request_JSON);

		for Index in range(len(Request_JSON["Songs"])):
			#Deprecated
			"""
			Proxy_Request = {
				"URL": Request_JSON["Songs"][Index]["Proxied_URL"],
				"Headers": Request_JSON["Proxied_Headers"]
			}
			File_Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/proxy", json=json.dumps(Proxy_Request, indent=0), timeout=60);
			"""



			Log.Info(f"Downloading Tunnelled File at {Request_JSON["Songs"][Index]["Music_URL"]}...");
			while (True):
				File_Request: httpx.Response = httpx.get(url=Request_JSON["Songs"][Index]["Music_URL"], timeout=5);
				match File_Request.status_code:
					case 418:
						Log.TSN_Debug(f"The server didn't finish downloading the file, retrying in a second."); time.sleep(1); continue;
					case 404: Log.Fetch_ALog().ERROR(f"The server told us the song was never downloaded!"); return;
					case 500: Log.Fetch_ALog().ERROR(f"The server couldn't download the song successfully!"); return;
					case _: break;
			
			File.Path_Require("Downloads/");
			with open(f"Downloads/{Request_JSON["Songs"][Index]["File_Name"]}", "wb") as Music:
				Music.write(File_Request.content);
			Log.Fetch_ALog().OK();

	except Exception as Except: Log.Fetch_ALog().EXCEPTION(Except, True);

Request_Handler("https://soundcloud.com/klausveen/klaus-veen-ordinary-days-v2?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"); # Soundcloud - 1 Song
# ↑ This is used for the README's Example /fetch JSON.

#Request_Handler("https://lexycat.bandcamp.com/album/heartstrings"); # Bandcamp (Album)
#Request_Handler("https://on.soundcloud.com/piimuKbl3a7KDMDGxP"); # Soundcloud (Album)
#Request_Handler("https://www.youtube.com/watch?v=gvPaMPeGwqg"); # YT
#Request_Handler("https://www.fuckshit.com/watch?v=gvPaMPeGwqg"); # Invalid