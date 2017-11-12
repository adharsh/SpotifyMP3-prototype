import re
import os
import urllib
import urllib.parse
import urllib.request

import youtube_dl

APIkey = 'AIzaSyBUbP-LKAnh6vdarxh-gXXfBp3dPZnyL8k'

search_keywords = []
with open('tmptitles.txt') as my_file:
    for line in my_file:
        search_keywords.append(line)

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

os.remove('tmptitles.txt')