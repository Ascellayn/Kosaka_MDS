from KMDS.Globals import *;
import os;

def URL_Safe(String: str) -> str:
	return String\
.replace("!", "%21")\
.replace("#", "%23")\
.replace("$", "%24")\
.replace("&", "%26")\
.replace("'", "%27")\
.replace("(", "%28")\
.replace(")", "%29")\
.replace("*", "%2A")\
.replace("+", "%2B")\
.replace(",", "%2C")\
.replace("/", "⧸")\
.replace(":", "%2A")\
.replace(";", "%2B")\
.replace("=", "%3D")\
.replace("?", "%3F")\
.replace("@", "%40")\
.replace("[", "%5B")\
.replace("]", "%5D");

#.replace("/", "%2F")\

def isOpus(Information: dict) -> bool:
	if ("entries" in Information.keys()):
		if (Information["entries"][0]["ext"] == "opus"): return True;
	elif (Information["ext"] == "opus"): return True;

	return False;

def Default_Options() -> dict:
	return {
		"cookiefile": "Cookies.txt",
		"format": "bestaudio/best",
		"outtmpl": os.path.join("Cache", "%(title)s.%(ext)s"),
		"writethumbnail": False,
	};

""" Unused due to race conditions
def Download_Hook(Information: dict) -> None:
	if (Information["status"] == "finished"):
		if (Information['filename'][-4:] == "opus"):
			File_Name = f"{Information['filename'][:-4]}ogg";
		else: File_Name = Information["filename"];
		Information[File_Name] = "finished";
		#with open(File_Name, "rb") as Music:
		#	Local_Files[File_Name] = Music.read();
"""




class AnnounceFinished(yt_dlp.postprocessor.common.PostProcessor):
	def __init__(self, downloader=None):super().__init__(downloader);

	def run(self, Information: dict) -> None:
		File_Name = Information["filepath"];
		Local_Files[File_Name] = "finished";
		Log.Info(f"Finished downloading {File_Name}.");
		return [], Information;


def Download_Thread(URL: str, Opus: bool) -> None:
	Log.Debug(f"Downloading {URL}...");
	Options: dict = Default_Options();
	if (Opus):
		Log.Debug(f"Opus conversion required for {URL}!"); 
		Options["postprocessors"] = [
			{
				"key": "FFmpegExtractAudio",
				"preferredcodec": "vorbis",
				"preferredquality": "quality"
			}
		];
	#Options["progress_hooks"] = [Download_Hook];

	with yt_dlp.YoutubeDL(Options) as YDL:
		YDL.add_post_processor(AnnounceFinished(YDL));
		YDL.download([URL]);
		Log.Fetch_ALog().OK();




def Fetch_Information(Request: dict) -> dict:
	with yt_dlp.YoutubeDL(Default_Options()) as YDL:
		Raw_Information = YDL.sanitize_info((YDL.extract_info(Request["URL"], download=False)));
		Misc.Thread_Start(Download_Thread, (Request["URL"], isOpus(Raw_Information)), True)
	URL_ID: str = Raw_Information["id"];

	if (Debug_Mode): File.JSON_Write(F"DEBUG-API/{URL_ID}.json", Raw_Information);

	# Flask Return Data & Caching Logic
	Information: dict = {
		"Status": 200,
		"ID": Raw_Information["id"],
		"Songs": []
	};

	if ("entries" not in Raw_Information.keys()):
		File_Title = Raw_Information['fulltitle'].replace("/", "⧸");
		File_Name = f"{File_Title}.{Raw_Information["ext"] if (not isOpus(Raw_Information)) else "ogg"}";
		Information["Songs"].append({
			"File_Name": File_Name,
			#"Proxied_URL": Raw_Information['url'],
			"Tunnel_URL": f"/tunnel?file={URL_Safe(File_Name)}",
			"Cover_URL": Raw_Information["thumbnail"],
			#"Cover_Name": f"{File_Title}.{Raw_Information["thumbnail"][-3:]}",
			"Metadata": {
				"Title": File_Title,
				"Artist": Raw_Information["uploader"],
				"Album": Raw_Information.get("album", None),
				"Track_Number": Raw_Information.get("track_number", None),
				"Track_Total": None,
				"Duration": Raw_Information["duration"],
				"Approximate_Size": Raw_Information["filesize_approx"]
			}
		});
		Local_Files[f"Cache/{File_Name}"] = "downloading";
		#Information["Proxied_Headers"] = Raw_Information["http_headers"];
	else:
		for Entry in Raw_Information["entries"]:
			if ("track" in Entry.keys()):
				File_Title = Entry["track"].replace("/", "⧸");
			else: File_Title = Entry["fulltitle"].replace("/", "⧸");
			
			File_Name = f"{Entry["fulltitle"]}.{Entry["ext"] if (not isOpus(Raw_Information)) else "ogg"}";
			Information["Songs"].append({
				"File_Name": File_Name,
				#"Proxied_URL": Entry["url"],
				"Tunnel_URL": f"/tunnel?file={URL_Safe(File_Name)}",
				"Cover_URL": Entry["thumbnail"],
				#"Cover_Name": f"{File_Title}.{Entry["thumbnail"][-3:]}",
				"Metadata": {
					"Title": File_Title,
					"Artist": Entry["uploader"],
					"Album": Entry.get("album", None),
					"Track_Number": Entry.get("track_number", None),
					"Track_Total": len(Raw_Information["entries"]),
					"Duration": Entry["duration"],
					"Approximate_Size": Entry["filesize_approx"]
				}
			});
			Local_Files[f"Cache/{File_Name}"] = "downloading";
		#Information["Proxied_Headers"] = Raw_Information["entries"][0]["http_headers"];
	
	# We set Local_Files[File_Name] here just in case to avoid race conditions with the client, though technically setting these also create a race condition.. This time with the download thread, however the odds of it being faster than the information return are probably zero.
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