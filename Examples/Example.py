from TSN_Abstracter import *;
import httpx;

Log.Clear();

Root_CFG: dict = File.JSON_Read("../Root_CFG.json");
WebServer_URL: str = f"http://{Root_CFG['WebServer']['Host']}:{Root_CFG['WebServer']['Port']}";


# Fetch Example
#Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=File.Read("Fetch_YT.json"), timeout=60);
#try: print(Request.json());
#except: Misc.Void();

Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=File.Read("Fetch_SC.json"), timeout=60);
try: print(Request.json());
except: Misc.Void();

#Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=File.Read("Fetch_BC.json"), timeout=60);
#try: print(Request.json());
#except: Misc.Void();

#Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=File.Read("Fetch_Invalid.json"), timeout=60);
#try: print(Request.json());
#except: Misc.Void();