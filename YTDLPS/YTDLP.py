from YTDLPS.Globals import *;
import os, threading;

def Fetch_Information(Request: dict) -> dict:
	Options: dict = {
		"format": "bestaudio/best",
		"outtmpl": os.path.join("Cache", '%(title)s.%(ext)s'),
		'writethumbnail': False
	};
	with yt_dlp.YoutubeDL(Options) as YDL:
		Raw_Information = YDL.sanitize_info((YDL.extract_info(Request["URL"], download=False)));
		URL_ID: str = Raw_Information["id"];

		# DEBUG
		if (Debug_Mode): File.JSON_Write(F"DEBUG-API/{URL_ID}.json", Raw_Information);

		# Flask Return Data & Caching Logic
		Information: dict = {
			"Status": 200,
			"ID": Raw_Information["id"],
			"Songs": []
		};

		if ("entries" not in Raw_Information.keys()):
			File_Title = Raw_Information['fulltitle']; 
			Information["Songs"].append({
				"File_Name": f"{File_Title}.{Raw_Information["ext"]}",
				"Music_URL": Raw_Information['url'],
				"Cover_URL": Raw_Information["thumbnail"],
				"Cover_Name": f"{File_Title}.{Raw_Information["thumbnail"][-3:]}",
				"Metadata": {
					"Title": File_Title,
					"Artist": Raw_Information["uploader"],
					"Album": Raw_Information.get("album", None),
					"Track_Number": Raw_Information.get("track_number", 0),
					"Duration": Raw_Information["duration"],
					"Approximate_Size": Raw_Information["filesize_approx"]
				}
			});
			Information["Proxied_Headers"] = Raw_Information["http_headers"];
		else:
			for Entry in Raw_Information["entries"]:
				File_Title = Entry['fulltitle'];
				Information["Songs"].append({
					"File_Name": f"{File_Title}.{Entry["ext"]}",
					"Music_URL": Entry['url'],
					"Cover_URL": Entry["thumbnail"],
					"Cover_Name": f"{File_Title}.{Entry["thumbnail"][-3:]}",
					"Metadata": {
						"Title": File_Title,
						"Artist": Entry["uploader"],
						"Album": Entry.get("album", None),
						"Track_Number": Entry.get("track_number", 0),
						"Duration": Entry["duration"],
						"Approximate_Size": Entry["filesize_approx"]
					}
				});
			Information["Proxied_Headers"] = Raw_Information["entries"][0]["http_headers"];

		"""
		File.JSON_Write(F"Cache/{URL_ID}.json", {
			"Download_Date": Time.Get_Unix(),
			"Metadata": Information["Songs"]
		});
		"""

		return Information;


"""class Proxied_Download:
	def __init__(self, URL):
		self.URL: str = URL;
		self.File_Name: str = None;
		self.Lock_File: threading.Lock = threading.Lock();
		self.Finished: bool = False;
		self.Chunks: list[bytes] = [];
		self.Offset: int = 0;

		Misc.Thread_Start(Function=self.Init_Download, Daemon=True);

	def Hook(self, Information):
		if (self.File_Name == None): self.File_Name = Information["filename"];
		with self.Lock_File:
			try:
				with open(self.File_Name, "rb") as Music:
					Music.seek(self.Offset);
					Data: bytes = Music.read();
					if (len(Data) != 0):
						self.Chunks.append(Data);
						self.Offset += len(Data);
			except: Misc.Void();
		if (Information["status"] == "finishied"): self.Finished = True;

	def Init_Download(self) -> None:
		Options: dict = {
			"outtmpl": os.path.join("Cache", '%(title)s.%(ext)s'),
			"progress_hooks": [self.Hook]
		};
		with yt_dlp.YoutubeDL(Options) as YDL:
			YDL.download(self.URL);

	def Stream(self):
		while (not self.Finished and self.Chunks != []):
			if (len(self.Chunks) != 0):
				yield self.Chunks(0);
			else: yield None;
		os.remove(self.File_Name);"""