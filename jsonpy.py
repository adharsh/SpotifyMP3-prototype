import json
from pprint import pprint

from collections import namedtuple

SongData = namedtuple("SongData", "name artists")
data = []

raw_data = json.load(open('data.json'))

for i in range(0, len(raw_data["tracks"]["items"])):
    track = raw_data["tracks"]["items"][i]["track"]
    track_name = track["name"]
    track_artists = []

    for a in range(0, len(track["artists"])):
        track_artists.append(track["artists"][a]["name"])
    data.append(SongData(name=track_name, artists=track_artists))
    
for i in range(0, len(data)):
    dataidk = ""
    for a in range(0, len(data[i].artists)):
        dataidk += data[i].artists[a] + ", "
    print(data[i].name + ": " + dataidk)
