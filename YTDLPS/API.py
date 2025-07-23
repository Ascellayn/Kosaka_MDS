from YTDLPS.Globals import *;
from YTDLPS.YTDLP import *;
import re;

API = flask.Flask(__name__);

@API.route("/", methods=["GET"])
def Root(): return Root_CFG;

@API.route("/fetch", methods=["POST"])
def Fetch():
	AL_Request: Log.Awaited_Log = Log.Info(f"Received request from {flask.request.host}...");
	try: Request: dict = json.loads(flask.request.get_json());
	except Exception as Except:
		AL_Request.ERROR(Except)
		flask.abort(400);

	URL: str = Request["URL"];
	Log.Info(f"Requested URL: {URL}");
	
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
