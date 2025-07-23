from YTDLPS.Globals import *;
import os;

def Fetch_Information(Request: dict) -> dict:
	Options: dict = {
		"format": "bestaudio/best",
		"outtmpl": os.path.join("Cache", '%(title)s.%(ext)s'),
		'writethumbnail': True
	};
	with yt_dlp.YoutubeDL(Options) as YDL:
		Raw_Information = YDL.sanitize_info((YDL.extract_info(Request["URL"], download=False)));
		Cache: bool = True; URL_ID: str = Raw_Information["id"];

		# DEBUG
		if (Debug_Mode): File.JSON_Write(F"DEBUG-API/{URL_ID}.json", Raw_Information);

		# Download Logic
		if (not File.Exists(F"Cache/{URL_ID}.json")):
			YDL.download(Request["URL"]); Cache = True;

		# Flask Return Data & Caching Logic
		Information: dict = {
			"Status": 200,
			"Cached": Cache,
			"ID": Raw_Information["id"],
			"Songs": []
		};

		if ("entries" not in Raw_Information.keys()):
			File_Title = Raw_Information['fulltitle']; 
			Information["Songs"] = {
				"File_Location": f"{os.getcwd()}/Cache/{File_Title}.{Raw_Information["ext"]}",
				"Metadata": {
					"Title": File_Title,
					"Artist": Raw_Information["uploader"],
					"Album": Raw_Information.get("album", None),
					"Track_Number": Raw_Information.get("track_number", 0),
					"Duration": Raw_Information["duration"],
				}
			};
		else:
			for Entry in Raw_Information["entries"]:
				File_Title = Entry['fulltitle'];
				Information["Songs"].append({
					"File_Location": f"{os.getcwd()}/Cache/{File_Title}.{Entry["ext"]}",
					"Metadata": {
						"Title": File_Title,
						"Artist": Entry["uploader"],
						"Album": Entry.get("album", None),
						"Track_Number": Entry.get("track_number", 0),
						"Duration": Entry["duration"],
					}
				});

		File.JSON_Write(F"Cache/{URL_ID}.json", {
			"Download_Date": Time.Get_Unix(),
			"Metadata": Information["Songs"]
		});

		return Information;