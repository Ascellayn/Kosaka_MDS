from KMDS.Globals import *;
from KMDS.YTDLP import *;

API = flask.Flask(__name__);

@API.route("/", methods=["GET"])
def Root() -> None: return Root_CFG;

@API.route("/fetch", methods=["POST"])
def Fetch() -> None:
	AL_Request: Log.Awaited_Log = Log.Info(f"Received Fetch Request from {flask.request.host}...");
	try: Request: dict = json.loads(flask.request.get_json());
	except Exception as Except:
		AL_Request.ERROR(Except)
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
			"Error": "No valid URLs were provided!"
		}

	Reply: dict = Fetch_Information(Request);
	AL_Request.OK(); return Reply;

@API.route("/proxy", methods=["POST"])
def Proxy() -> None:
	AL_Request: Log.Awaited_Log = Log.Info(f"Received Proxy Request from {flask.request.host}...");
	try:
		Request: dict = json.loads(flask.request.get_json());
		Proxied_URL: str = Request["URL"];
		Proxied_Headers: str = Request["Headers"];
		Proxied_Headers["Accept-Encoding"] = "identity";
	except Exception as Except:
		AL_Request.ERROR(Except)
		flask.abort(400);

	Log.Info(f"Proxy URL: {Proxied_URL}");

	def Stream_Proxy():
		Audio_File: bytes = b""; Download_Unix: int = Time.Get_Unix();
		with httpx.stream(method="GET", url=Proxied_URL, headers=Proxied_Headers, follow_redirects=False) as Stream:
			for Chunk in Stream.iter_bytes():
				Audio_File += bytes(Chunk);
				Download_Speed = round((len(Audio_File) / 10**6) / ((Time.Get_Unix() - Download_Unix) if (Time.Get_Unix() - Download_Unix) != 0 else 1), 2);
				Log.Carriage(f"Download Speed: {Download_Speed}mb/s");
				yield Chunk;
		Log.Info(f"Finished Proxy-ing File with a speed of {Download_Speed}MB/s.")


	return Stream_Proxy();