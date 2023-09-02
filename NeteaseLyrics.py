import cloudmusic

Playlist = cloudmusic.getPlaylist(620094419)
for i in Playlist:
    try:
        Lyrics = i.getLyrics()
        Name = i.name
        Artist = i.artist
        File = open(Name + ' - ' + ','.join(Artist) + '.lrc','w')
        File.write('\n'.join(i.getLyrics()))
        File.close()
    except:
        pass
