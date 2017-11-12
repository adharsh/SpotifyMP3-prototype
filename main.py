import json
import re
import os
import urllib
import urllib.parse
import urllib.request
import youtube_dl
import sys
import shutil
import stat 
import timeit

from threading import Thread
from time import sleep
from pprint import pprint
from collections import namedtuple


#mulithreading
#GUI - youtube link + title, thumbnail
#change api key if needed - https://developer.spotify.com/web-api/console/get-playlist/
#stackoverflow
#handle case of invalid link - yup
#save in folder - plalylist name - yup

#url = input('Enter URL: ')
#NUM_THREADS = input('Enter number of threads: (10-20 is good))) actually find possible value yourself

start = timeit.default_timer()


url = 'https://open.spotify.com/user/sciencelord01/playlist/2SdH4KGzHPmqLAbqUA9GqB'

val = url.find('user')
if val < 0:
    print("Invalid URL Entered")
    sys.exit()

retrieved_data = url[val + 5:].split('/')

user = retrieved_data[0]
id = retrieved_data[2]

spotifyAPIkey = str([line.rstrip('\n') for line in open('oauthkey.txt')])[2:][:-2]

os.system('curl -s -X GET "https://api.spotify.com/v1/users/' + user + '/playlists/' + id + '" -H Accept: "application/json" -H "Authorization: Bearer "' + spotifyAPIkey + '> tmpPlaylist.json')

SongData = namedtuple("SongData", "name artists")
data = []

raw_data = json.load(open('tmpPlaylist.json'))

if json.dumps(raw_data).find('error') > 0:
    print(str(raw_data["error"]["status"]) + ": " + raw_data["error"]["message"] + " -> Spotify")
    print("If needed, get key at: " + "https://developer.spotify.com/web-api/console/get-playlist/");
    sys.exit()

folder_name = raw_data["name"]

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

youtubeAPIkey = 'AIzaSyBUbP-LKAnh6vdarxh-gXXfBp3dPZnyL8k'

if not os.path.isdir(folder_name):
    os.makedirs(folder_name)
else:
    response = input("Playlist already exists. Clear playlist? (y/n): ")
    if response != "n":
        for filename in os.listdir(folder_name):
            os.chmod(folder_name + "/" + filename, stat.S_IWUSR)
            os.remove(folder_name + "/" + filename)
    else:
        print("Done.")
        sys.exit()        

video_ids = []

for q in search_keywords:
    q += 'topic'
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + q + '&maxResults=1&key=' + youtubeAPIkey
    headers = {}
    headers ['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()  
    nextPageToken = re.findall('"nextPageToken": "(.*?)"', str(respData))
    individual_video_id = re.findall('"videoId": "(.*?)"', str(respData))
    
    video_ids.append(individual_video_id)

NUM_THREADS = 10
NUM_THREADS = len(video_ids) if len(video_ids) < NUM_THREADS else NUM_THREADS

thread_ids = []
threads = []

for i in range(0, NUM_THREADS):
    thread_ids.append([])

for i in range(0, len(video_ids)):
    thread_ids[i%NUM_THREADS].append(video_ids[i])

def downloadThreadFunc(folderName, listVids):    
    for i in listVids:
        os.system('youtube-dl --extract-audio --audio-format "mp3" --output "' + folderName + '/%(title)s.%(ext)s" "https://www.youtube.com/watch?v="' + str(i)[2:][:-2] + "")
    sleep(1)

for i in range(0, NUM_THREADS):
    # pprint(str(i) + ": " + str(thread_ids[i]))
    thread = Thread(target = downloadThreadFunc, args = (folder_name, thread_ids[i]))
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

#os.remove('*.webm')
os.remove('tmpPlaylist.json')
print("Done.")

stop = timeit.default_timer()

print (str(NUM_THREADS) + " threads take (secs): " + str(stop - start ))