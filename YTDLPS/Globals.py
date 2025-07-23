from TSN_Abstracter import *;
import flask, httpx, json, re, yt_dlp;

Root_CFG = File.JSON_Read("Root_CFG.json");
Debug_Mode: bool = Root_CFG["Debug"];
YTDLPS_Version: str = Root_CFG["Version"];
