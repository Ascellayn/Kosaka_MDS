from YTDLPS.Globals import *;

def Fetch_Information(Request: dict) -> dict:
	with yt_dlp.YoutubeDL({}) as YDL:
		Information = YDL.sanitize_info((YDL.extract_info(Request["URL"], download=False)));
		File.JSON_Write("DEBUG-API/Fetch_Information.json", Information)
		return Information;