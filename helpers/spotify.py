"""
Copyright (c) 2022, Zach Lagden
All rights reserved.
"""

# <--- Imports --->

import spotipy
import json

from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from urllib.parse import urljoin, urlparse
from configparser import ConfigParser

config = ConfigParser()
config.read('./configs/music.ini')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.get(
    "SPOTIFY", "client_id"), client_secret=config.get("SPOTIFY", "client_secret")))


class ConfigFileDataIncorrect(Exception):
    pass


try:
    _ = sp.track("https://open.spotify.com/track/5K9tfeoiztw94dyWzF39jq?si=65c9b47a72f14714")
    del _
except:
    raise ConfigFileDataIncorrect(
        "Spotify API Credentials Invalid, Please put your 'client_id' and 'client_secret' into the 'spotify.ini' file.")


class Spotify:
    def get_youtube_urls(url: str = None):
        if not url:
            return None

        url = urljoin(url, urlparse(url).path)
        link_list = []

        if "/track/" in url:
            spotify_track_data = json.loads(json.dumps(sp.track(url)))

            youtube_query = f'{spotify_track_data["name"]} - {spotify_track_data["artists"][0]["name"]}'
            youtube_results = VideosSearch(youtube_query, limit=1).result()['result']
            youtube_url = f"https://www.youtube.com/watch?v={youtube_results[0]['id']}"

            return [youtube_url]

        elif "/playlist/" in url:
            spotify_playlist_data = json.loads(json.dumps(sp.playlist(url)))

            for song in spotify_playlist_data["tracks"]["items"]:
                youtube_query = f'{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}'

                youtube_results = VideosSearch(youtube_query, limit=1).result()['result']
                link_list.append(f"https://www.youtube.com/watch?v={youtube_results[0]['id']}")

            return link_list

        elif "/album/" in url:
            spotify_album_data = json.loads(json.dumps(sp.album(url)))

            for song in spotify_album_data["tracks"]["items"]:
                youtube_query = f'{song["name"]} - {song["artists"][0]["name"]}'

                youtube_results = VideosSearch(youtube_query, limit=1).result()['result']
                link_list.append(f"https://www.youtube.com/watch?v={youtube_results[0]['id']}")

            return link_list

        else:
            return []


class SpotifyGenerator:
    def get_youtube_urls(url: str = None):
        if not url:
            return None

        url = urljoin(url, urlparse(url).path)

        if "/track/" in url:
            spotify_track_data = json.loads(json.dumps(sp.track(url)))

            youtube_query = f'{spotify_track_data["name"]} - {spotify_track_data["artists"][0]["name"]}'
            youtube_results = VideosSearch(youtube_query, limit=1).result()['result']
            youtube_url = f"https://www.youtube.com/watch?v={youtube_results[0]['id']}"

            yield youtube_url

        elif "/playlist/" in url:
            spotify_playlist_data = json.loads(json.dumps(sp.playlist(url)))

            for song in spotify_playlist_data["tracks"]["items"]:
                youtube_query = f'{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}'

                yield youtube_query

        elif "/album/" in url:
            spotify_album_data = json.loads(json.dumps(sp.album(url)))

            for song in spotify_album_data["tracks"]["items"]:
                youtube_query = f'{song["name"]} - {song["artists"][0]["name"]}'

                yield youtube_query

        else:
            yield None
