import json
import re
import os
import urllib
import urllib.parse
import urllib.request
import youtube_dl
from pprint import pprint
from collections import namedtuple

#change api key
#save in folder
#GUI
# url = input('Enter URL: ')
url = 'https://open.spotify.com/user/sciencelord01/playlist/1matOZfpk9zIYw263oaypd'

retrieved_data = url[30:].split('/')

user = retrieved_data[0]
id = retrieved_data[2]

os.system('curl -s -X GET "https://api.spotify.com/v1/users/' + user + '/playlists/' + id + '" -H Accept: "application/json" -H "Authorization: Bearer BQD6AAs_zKpNPUqTUXucgwml4pR4EN2rklMop2AhwinMCK2WbQaCIXZv_E7SmFD6LOchWXHv73U6IK7Hcmi0SVW-pTc8foDlwB3kb3HSa7C6wHu5kyu-G66PYuudjcdOVwDAsfP6SoPxemg" > tmpPlaylist.json')

SongData = namedtuple("SongData", "name artists")
data = []

raw_data = json.load(open('tmpPlaylist.json'))

for i in range(0, len(raw_data["tracks"]["items"])):
    track = raw_data["tracks"]["items"][i]["track"]
    track_name = track["name"]
    track_artists = []

    for a in range(0, len(track["artists"])):
        track_artists.append(track["artists"][a]["name"])
    data.append(SongData(name=track_name, artists=track_artists))

search_keywords = []
for i in range(0, len(data)):
    query = data[i].name + ": "
    for a in range(0, len(data[i].artists)):
        query += data[i].artists[a] + ", "
    search_keywords.append((query[:-3] + " topic").replace(" ", "+"))

APIkey = 'AIzaSyBUbP-LKAnh6vdarxh-gXXfBp3dPZnyL8k'

for q in search_keywords:
    q += 'topic'
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + q + '&maxResults=1&key=' + APIkey
    headers = {}
    headers ['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()  
    nextPageToken = re.findall('"nextPageToken": "(.*?)"', str(respData))

    video_id = re.findall('"videoId": "(.*?)"', str(respData))

    for i in video_id:
        os.system('youtube-dl --extract-audio --audio-format "mp3" --output "%(title)s.%(ext)s" "https://www.youtube.com/watch?v="' + i)
        #os.system('youtube-dl --extract-audio --audio-format "mp3" --output "%(title)s.%(ext)s" "https://www.youtube.com/watch?v="' + i)
        
#os.remove('*.webm')
os.remove('tmpPlaylist.json')