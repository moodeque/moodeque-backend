import requests
import json
import os
from hashlib import md5
from urllib import urlencode, quote, quote_plus
from urlparse import urlparse
from oauth_hook import OAuthHook
from mutagen.mp3 import MP3
from moodeque.models import Song

class StereoMoodClient(object):
  POOR_AUTH_URL = "http://www.stereomood.com/api/hackitaly/auth.php"
  SEARCH_URL = "http://www.stereomood.com/api/search.json?q=%s&type=%s&limit=%d"

  def __init__(self, api_key, secret_key, user, password, auth_on_init=True):
    self.api_key = api_key
    self.secret_key = secret_key
    self.user = user
    self.password = md5(password).hexdigest()

    # Must use a tuple for the right order of the parameters
    # O_O
    params = (
      ("key", self.api_key), 
      ("secret", self.secret_key),
      ("username", self.user),
      ("password", self.password),
    )

    self.signature = md5(urlencode(params)).hexdigest()
    self.oauth_token = ""
    self.oauth_token_secret = ""

    if auth_on_init:
      self.authenticate()

  def is_authenticated(self):
    return self.oauth_token and self.oauth_token_secret

  def authenticate(self):
    params = {
      "key": self.api_key, 
      "username": self.user,
      "password": self.password,
      "signature": self.signature
    }

    response = requests.get(self.POOR_AUTH_URL, params=params)
    for token in response.text.split("&"):
      k,v = token.split("=")
      self.__dict__[k] = v

    oauth_hook = OAuthHook(self.oauth_token, self.oauth_token_secret, self.api_key, self.secret_key, True)
    self.client = requests.session(hooks={'pre_request': oauth_hook})

  def search_by_mood(self, mood, limit):
    return self.search_by('mood', mood, limit)

  def search_by_activity(self, activity, limit):
    return self.search_by('activity', activity, limit)

  def search_by_site(self, site, limit):
    return self.search_by('site', site, limit)

  def search_by(self, type, q, limit):
    if type not in ('mood', 'activity', 'site'):
      return None

    response = self.client.get(self.SEARCH_URL % (quote_plus(q), type, limit))
    return self.build_song_list(response.text)

  def download_song(self, song, save_dir):
    path = os.path.join(save_dir, song.id) + ".mp3"

    if not os.path.exists(path):
      with open(path, "w") as f:
        response = self.client.get(song.audio_url)
        f.write(response.content)

    audio = MP3(path)
    song.length = int(audio.info.length)
    song.local_path = path

    return song

  def build_song_list(self, text):
    return [Song(**s) for s in json.loads(text).get('songs', [])]
