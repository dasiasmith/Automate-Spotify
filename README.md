Portfolio

## About

This script takes in a user's liked YouTube videos and generates a Spotify playlist based on songs in the liked playlist.

## Credits

[Code Credit to The Come Up Code](github.com/TheComeUpCode/SpotifyGeneratePlaylist)

## Table of Contents

  * [Technologies](#technologies)

  * [Usage](#usage)

  * [Troubleshooting](#Troubleshooting)

## Technologies

* [YouTube Data API v3](https://developers.google.com/youtube/v3)
* [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
* [Requests Library v 2.22.0](https://docs.python-requests.org/en/master/)
* [Youtube_dl v 2020.01.24](https://github.com/ytdl-org/youtube-dl/)

## Usage

1. Install All Dependencies

```
  pip3 install -r requirements.txt
```

2. Collect your Spotify User ID and Oauth Token from Spotify and add it to secrete.py file

3. Enable Oauth for Youtube and download the client_secretes.json. See guide here: [Set Up YouTube Oauth](https://developers.google.com/youtube/v3/getting-started)

4. Run the file using:

```
python3 create_playlist.py
```
## Troubleshooting

* Spotify Oauth token expires very quickly, if you come across a ```KeyError``` this could be caused by an expired token. Refer back to the Spotify Web API page to generate a new token. 