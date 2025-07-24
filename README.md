# Kosaka Media Downloading Service (KMDS)
A YT-DLP/Flask Wrapper built specifically for the extremely strange conditions caused by The Sirio Network's infrastructure skill issues, for Kosaka.  
TSN's Infrastructure is definitely quite a mess, have the following in mind:
- Kosaka is hosted on "A1F"
- The Media Server MUST be hosted on "E2B" (because A1F also hosts a VPN, and obviously I do not wish my VPN IP's to get sent to the void fields by Google)
- E2B is an EXTREMELY weak server with negative amounts of RAM
- Both A1F and E2B save their files to the same shared drive
- A1F and E2B, despite having different public ips, are in fact very much in the same private network.

So now you somewhat maybe understand why I don't just use YT-DLP directly in Kosaka's code and why I'm doing extremely weird things to have the result that I want.  
As I'm writing (v1.0rc1), I'm still not doing *exactly* what I want however:  
I'd rather download the files via KMDS once and then have Kosaka directly pull from KMDS's Cache the files it needs, because the shared drive nature of TSN's Infrastructure let's me do ungodly cursed things such as this. It'd improve performance significantly more because I wouldn't have to basically "download" the same file twice.  
I would do this but I've delayed Kosaka's v2.4.0 release a ***little bit too much already***...

<br>

## Usage
- Initiate a GET Request at http://[KMDS]/ to get KMDS's Root_CFG JSON File.
- Initiate a POST Request at http://[KMDS]/fetch with the following JSON Data:
```json
{
	"URL": "[Either a YouTube/Soundcloud/Bandcamp Link]"
}
```
- KMDS will return a JSON File similar to this:
```json
{
  "ID": "433445760", # To be removed
  "Proxied_Headers": { # To be removed
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.5",
    "Sec-Fetch-Mode": "navigate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
  },
  "Songs": [
    {
      "Cover_Name": "Klaus Veen - Ordinary Days V2.jpg", # To be removed
      "Cover_URL": "https://i1.sndcdn.com/artworks-000338473992-8da1lw-original.jpg",
      "File_Name": "Klaus Veen - Ordinary Days V2.m4a", # To be removed
      "Metadata": {
        "Album": null,
        "Approximate_Size": 7122360, # To be removed
        "Artist": "Klaus Veen",
        "Duration": 356.118,
        "Title": "Klaus Veen - Ordinary Days V2",
        "Track_Number": 0 # This is 0 if the song isn't part of an Album, otherwise it will have a non-null value.
      },
      "Music_URL": "http://[KMDS]/tunnel?file=Klaus Veen - Ordinary Days V2.m4a",
      "Proxied_URL": "https://playback.media-streaming.soundcloud.cloud/CVBDMoZS2xxV/aac_160k/b323473d-8012-4965-8950-00061e0833e6/playlist.m3u8?expires=1753391795&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wbGF5YmFjay5tZWRpYS1zdHJlYW1pbmcuc291bmRjbG91ZC5jbG91ZC9DVkJETW9aUzJ4eFYvYWFjXzE2MGsvYjMyMzQ3M2QtODAxMi00OTY1LTg5NTAtMDAwNjFlMDgzM2U2L3BsYXlsaXN0Lm0zdTg~ZXhwaXJlcz0xNzUzMzkxNzk1IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzUzMzkxNzk1fX19XX0_&Signature=vignGQA9tWjQubsV66eZSDkuy8jP8a7tmIg4EiX0vfvxbTA190DI2BZJ16Oiwzj8jA4sMiZ7DSP5LhReHK6p10cvzDisaIk4vHSNWvbftRo49w0HwP4wxF68MYWXOEm7jvwpyVw0CINqCO64dzgzKFmHMObbLCbbxUGFZMf2XVfNpxguPOBwIL5bXgUOHn4gEh3WEKQMp~pH-eJR-qqSzCzvPXtgeWw1oH77te5TXQrgL4IjVnzHr9xaoE0-dgmapuyVb38XcKUe-Ef9qMubavhLlPA7ApbNFpr~Xcsk3kmnQZhKTKJXolyz2wrSEvy-O6j5qpAnFb5nbDBkv5XoqA__&Key-Pair-Id=K34606QXLEIRF3" # To be removed
    }
  ],
  "Status": 200
}
```
- At the same time, KMDS launched a thread to download all the songs that the URL provides, ***it does not do ANY kind of processing EXCEPT for Opus files***.
- The most important part is ["Songs"]["Music_URL"], as you'll be then doing a GET request there.
- The server may then respond with the following status codes:
	- 200: The song's file will be sent.
	- 418: The file hasn't finished downloading yet. It is the client's responsibility to try again.
	- 500: The server encountered an error while downloading the file.
	- 400: Ya jinxed the request somehow (missing "file" argument)


## Dependencies
- [TSN_Abstracter v2.1.0 (or above)](https://github.com/Ascellayn/TSN_Abstracter)
- python3-flask
- python3-httpx
- python3-re
- yt-dlp
After you've figured (most likely) how in the name of fuck to install TSNA, all you have to do is run `main.py`, you may also run `Showcase.py` to do some test downloads.  
KMDS is not intended to be open to the internet, stay local folks.  

<br>

## W T F is this codebase?
This honestly was pulled out of my arse in about 8~ hours of work (which honestly isn't a lot to my standard), I had to go through a lot of trial and error, and objectively this is a very dodgy way of doing what I want. But hey if it ain't broke, don't fix it.  
I've had to fight at least 201 race conditions during the development of this tool.  

By the way there's basically no error handling lol, GOOD LUCK!

### may i fix it
what the hell is wrong with you digging in code as bad as this

<br>

###### Kosaka Media Downloading Service (KMDS) © 2025 by Ascellayn is licensed under TSN License 1.0 - Base