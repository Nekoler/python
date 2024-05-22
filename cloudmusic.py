#!/data/data/com.termux/files/usr/bin/python
from sys import argv
from json import loads
from requests import get

def para():
    if len(argv) != 3:
        print(f'Uasge:{argv[0]} <PlaylistId> <Quantity>')
        exit()

def download_url(song_id):
    api = 'https://autumnfish.cn/song/url'
    url = loads(get(api,params={'id':song_id}).text)['data'][0]['url']
    return url

def name_url(playlist_id,quantity):
    api = 'https://autumnfish.cn/playlist/track/all'
    playlist = loads(get(api,params={'id':playlist_id}).text)['songs'][:quantity]
    songs = []
    for i in playlist:
        name = i['name']
        ar = ','.join([j['name']for j in i['ar']])
        url = download_url(i['id'])
        songs.append('%s	%s - %s.mp3'%(url,name,ar))
    return songs
para()
open('/sdcard/Download/网易.txt','w').write('\n'.join(name_url(argv[1],int(argv[2]))))
