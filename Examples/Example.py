from TSN_Abstracter import *;
import httpx;

Root_CFG: dict = File.JSON_Read("../Root_CFG.json");
WebServer_URL: str = f"http://{Root_CFG['WebServer']['Host']}:{Root_CFG['WebServer']['Port']}";


# Fetch Example
Request: httpx.Request = httpx.post(url=f"{WebServer_URL}/fetch", json=File.Read("Fetch_Example.json"));
print(Request.json());