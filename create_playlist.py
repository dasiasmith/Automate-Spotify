"""
Step 1: Log Into Youtube
Step 2: Grab Our Liked Videos
Step 3: Create A New Playlist
Step 4: Search For the Song
Step 5: Add this song into the new Spotify Playlist
"""
import json
import requests
import os

from secrets import spotify_user_id, spotify_token
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class CreatePlaylist:

    def _init_(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    #Step 1: Log Into Youtube
    def get_youtube_client(self):
        # Copied from YouTube Data API
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        # From YouTube Data API
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        return youtube_client

    #Step 2: Grab Our Liked Videos and Creating a Dictionary of Important Song Information
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        # Collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # Use youtube_dl to collect the song name and artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]

            # Save all import info
            self.all_song_info[video_title] ={
                "youtube_url":youtube_url,
                "song_name":song_name,
                "artist":artist,

                # Add the url, easy to get song to put into playlist
                "spotify_uri":self.get_spotify_uri(song_name, artist)
            }

    #Step 3: Create A New Playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name":"YouTube Liked Vids",
            "description": "All Liked Youtube Videos",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # Playlist id
        return response_json["id"]

    #Step 4: Search For the Song
    def get_spotify_uri(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artists%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # Only use the first song
        url = songs[0]["url"]

        return url

    #Step 5: Add this song into the new Spotify Playlist
    def add_song_to_playlist(self):
        # Populate our songs dictionary
        self.get_liked_videos()

        # Collect all of uri
        uris = []
        for song,info in self.all_song_info.items():
            uris.append(info["spotify_uri"])

        # Create a new playlist
        playlist_id = self.create_playlist()

        # Add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlist/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        return response_json

tester = CreatePlaylist()
print(tester.create_playlist())    