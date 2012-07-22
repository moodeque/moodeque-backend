# part of moodeque

class Song(object):
    def __init__(self, songid, title, artist, album, url, image_url, audio_url, post_url):
        self.songid = songid
        self.title = title
        self.artist = artist
        self.album = album
        self.url = url
        self.image_url = image_url
        self.audio_url = audio_url
        self.post_url = post_url
        self.length = None
        self.local_path = None

    def __str__(self):
        return "#%s %s/%s by %s at %s" %(str(self.songid), str(self.album),
                                         str(self.title), str(self.artist),
                                         str(self.url))

