# part of moodeque

class Song(object):
    def __init__(self, id, title, artist, album, url, image_url, audio_url, post_url):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.url = url
        self.image_url = image_url
        self.audio_url = audio_url
        self.post_url = post_url
        self.length = None
        self.local_path = None

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            artist=self.artist,
            album=self.album,
            url=self.url,
            image_url=self.image_url,
            audio_url=self.audio_url,
            post_url=self.post_url,
            length=self.length,
            local_path=self.local_path)

    def __str__(self):
        return "#%s %s/%s by %s at %s" %(str(self.songid), str(self.album),
                                         str(self.title), str(self.artist),
                                         str(self.url))
