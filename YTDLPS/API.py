from YTDLPS.Globals import *;
from YTDLPS.YTDLP import *;

API = Flask(__name__);

@API.route("/", methods=["GET"])
def Root(): return Root_CFG;

@API.route("/fetch", methods=["POST"])
def Fetch():
	Request: dict = json.loads(request.get_json());
	AL_Request: Log.Awaited_Log = Log.Info(f"Received request from {request.host}...");
	try:
		Log.Info(f"Requested URL: {Request["URL"]}");
		Reply: dict = Fetch_Information(Request);
		AL_Request.OK(); return Reply;
	except Exception as Except:
		AL_Request.ERROR(Except)
		abort(400);