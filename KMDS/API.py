from KMDS.Globals import *;
from KMDS.YTDLP import *;

API = flask.Flask(__name__);

@API.route("/", methods=["GET"])
def Root() -> None: return Root_CFG;

@API.route("/fetch", methods=["POST"])
def Fetch() -> None:
	Log.Info(f"Received Fetch Request from {flask.request.host}...");
	try: Request: dict = json.loads(flask.request.get_json());
	except Exception as Except:
		Log.Fetch_ALog().EXCEPTION(Except)
		flask.abort(400);

	URL: str = Request["URL"];
	Log.Info(f"Fetch URL: {URL}");
	
	if (len(\
re.findall(r"youtube\.com/watch\?v=", URL) +\
re.findall(r"youtu\.be/", URL) +\
re.findall(r"youtube\.com/shorts/", URL)+\
re.findall(r"bandcamp\.com/album/", URL)+\
re.findall(r"bandcamp\.com/track/", URL)+\
re.findall(r"soundcloud\.com/\w*/", URL)+\
re.findall(r"on\.soundcloud\.com/", URL)
) == 0):
		return {
			"Status": 400,
			"Error": "The provided URLs is incorrect or isn't supported by KMDS!"
		}

	if (len(\
re.findall(r"youtube\.com/watch\?v=", URL) +\
re.findall(r"youtu\.be/", URL) +\
re.findall(r"youtube\.com/shorts/", URL)\
) != 0):
		ID_Lookup: list = re.findall(r"(?<=v=)[\w-_]*|(?<=shorts\/)[\w-_]*|(?<=youtu\.be\/)[\w-_]*", URL);
		if (len(ID_Lookup) != 0):
			Log.Warning(f"YouTube Link detected for \"{URL}\"! We are only going to care about the first video if it's a playlist link.");
			Request["URL"] = f"https://www.youtube.com/watch?v={ID_Lookup[0]}";

	Reply: dict = Fetch_Information(Request);
	Log.Fetch_ALog().OK(); return Reply;


# DEPRECATED: Can't figure out how the FUCK yt-dlp downloads YT files so fast, using this, YouTube throttles us to 0.3mb/s! Yikes!
@API.route("/proxy", methods=["POST"])
def Proxy() -> None:
	Log.Info(f"Received Proxy Request from {flask.request.host}...");
	try:
		Request: dict = json.loads(flask.request.get_json());
		Proxied_URL: str = Request["URL"];
		Proxied_Headers: str = Request["Headers"];
		Proxied_Headers["Accept-Encoding"] = "identity";
	except Exception as Except:
		Log.Fetch_ALog().EXCEPTION(Except);
		flask.abort(400);

	Log.Info(f"Proxy URL: {Proxied_URL}");

	def Stream_Proxy(Custom_Caller: str):
		Audio_File: bytes = b""; Download_Unix: int = Time.Get_Unix();
		with httpx.stream(method="GET", url=Proxied_URL, headers=Proxied_Headers, follow_redirects=False) as Stream:
			for Chunk in Stream.iter_bytes(1024):
				Audio_File += bytes(Chunk);
				Download_Speed = round((len(Audio_File) / 10**6) / ((Time.Get_Unix() - Download_Unix) if (Time.Get_Unix() - Download_Unix) != 0 else 1), 2);
				Log.Carriage(f"Download Speed: {Download_Speed}mb/s");
				yield Chunk;
		Log.Info(f"Finished Proxy-ing File with a speed of {Download_Speed}MB/s.");
		Log.Fetch_ALog(Custom_Caller).OK()

	return Stream_Proxy(Log.Get_Caller());


@API.route("/tunnel", methods=["GET"])
def Tunnel() -> None:
	Log.Info(f"Received Tunnel Request from {flask.request.host}...");
	try:
		Local_File: str = f"Cache/{flask.request.args['file']}";
	except Exception as Except:
		Log.Fetch_ALog().EXCEPTION(Except)
		flask.abort(400);
	
	#Log.Critical(json.dumps(Local_Files, indent=2));
	if (Local_File not in Local_Files.keys()): flask.abort(404);
	match Local_Files[Local_File]:
		case "downloading": flask.abort(418);
		case "error": del Local_Files[Local_File]; flask.abort(500);
	
	Log.Info(f"Tunneled File: {Local_File}");

	def __RAMTunnel_File():
		yield Local_Files[Local_File];
		del Local_Files[Local_File];
		os.remove(Local_File);

	def Tunnel_File(Custom_Caller: str):
		Upload_Unix: int = Time.Get_Unix();
		with open(Local_File, "rb") as Music:
			Audio_File: bytes = Music.read();
		yield Audio_File;
		Upload_Speed = round((len(Audio_File) / 10**6) / Misc.NotNull(Time.Get_Unix() - Upload_Unix));
		Log.Info(f"Finished Tunneling File with a speed of {Upload_Speed}MB/s.");
		del Local_Files[Local_File]; os.remove(Local_File);

		Log.Fetch_ALog(Custom_Caller).OK();

	return Tunnel_File(Log.Get_Caller());

