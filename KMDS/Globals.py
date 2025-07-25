from TSN_Abstracter import *;
import asyncio, flask, httpx, json, re, time, threading, yt_dlp;

Root_CFG: dict = File.JSON_Read("Root_CFG.json");
Debug_Mode: bool = Root_CFG["Debug"];
KMDS_Version: str = Root_CFG["Version"];

Local_Files: dict = {};