from TSN_Abstracter import *;
import asyncio, flask, httpx, json, os, re, time, threading, yt_dlp;

KMDS_Version: str = "v1.1.2";

Root_CFG: dict = File.JSON_Read("Root_CFG.json");
Debug_Mode: bool = Root_CFG["Debug"];
Root_CFG["Version"] = KMDS_Version;

Local_Files: dict = {};