from TSN_Abstracter import *;
import httpx, json, time;

Log.Clear();

Root_CFG: dict = File.JSON_Read("Root_CFG.json");
WebServer_URL: str = f"http://{Root_CFG['WebServer']['Host']}:{Root_CFG['WebServer']['Port']}";

def Request_Handler(URL: str) -> None:
	AL: Log.Awaited_Log = Log.Info(f"Fetching files for {URL}...")
	Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=json.dumps({"URL": URL}, indent=0), timeout=60);
	try:
		Request_JSON: dict = Request.json(); Log.Info(str(Request_JSON));
		if (Request_JSON["Status"] != 200): Log.Error(Request_JSON["Error"]); return;

		for Index in range(len(Request_JSON["Songs"])):
			""" Deprecated
			Proxy_Request = {
				"URL": Request_JSON["Songs"][Index]["Music_URL"],
				"Headers": Request_JSON["Proxied_Headers"]
			}
			File_Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/proxy", json=json.dumps(Proxy_Request, indent=0), timeout=60);
			"""

			AL: Log.Awaited_Log = Log.Info(f"Downloading Tunnelled File at {Request_JSON["Songs"][Index]["Music_URL"]}...");
			while (True):
				File_Request: httpx.Response = httpx.get(url=Request_JSON["Songs"][Index]["Music_URL"], timeout=60);
				match File_Request.status_code:
					case 418:
						Log.Warning(f"The server didn't finish downloading the file, retrying in a second.");
						time.sleep(1); continue;
					case 404: Log.Error(f"The server told us the song was never downloaded!");
					case 500: Log.Error(f"The server couldn't download the song successfully!");
					case _: break;

			File.Path_Require("Downloads/");
			with open(f"Downloads/{Request_JSON["Songs"][Index]["File_Name"]}", "wb") as Music:
				Music.write(File_Request.content);
			AL.OK();

	except Exception as Except:
		AL.ERROR(Except);
		raise Except;

#Request_Handler("https://lexycat.bandcamp.com/track/intro-heartpulse"); # Bandcamp
Request_Handler("https://on.soundcloud.com/piimuKbl3a7KDMDGxP"); # Soundcloud
#Request_Handler("https://www.youtube.com/watch?v=gvPaMPeGwqg"); # YT
#Request_Handler("https://www.fuckshit.com/watch?v=gvPaMPeGwqg"); # Invalid