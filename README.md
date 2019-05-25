# Spotify Discover Daily

Spotify Discover Daily creates new, personalized Spotify playlists to help you discover new music each day.

## The Playlists

**Discovery** contains the songs that you haven't yet listened to (beginning from the moment you authorized this app) from the playlists made by Spotify that you follow.

**Releaser** contains all the songs released in the past 4 weeks from your top 50 artists from the past 4 weeks and your top 50 artists from the past 6 months (according to Spotify).

**Top Tracks** contains your top 50 tracks from the past 4 weeks combined with your top 50 tracks from the past 6 months (according to Spotify).

Due to a current issue with Spotify, in some rare cases, a song will continue to appear in your Discovery playlist after you've listened to it. To prevent a song from reappearing in your Discovery playlist, add it to your **Remover** playlist.

These playlists update daily.

To manually update Discovery to not include the songs you just listened to, just come back to the web app and re-enter your Spotify username.

You must listen to at least 30 seconds of a song for it to count as a listen.

## How to Re-Create Spotify Discover Daily

* [Create a Spotify app](https://developer.spotify.com/dashboard/applications)

* Click Edit Settings, and add and save http://0.0.0.0:5000/authorization under Redirect URIs (Change 0.0.0.0:5000 if necessary)

* Download this repository and install `requirements.txt`

* Copy your Spotify app's Client ID and Client Secret into `secret.py`, and change the Redirect URI if necessary

* Create a Spotify account that you would like to use as the master account to own all the playlists that are created, and copy its username into `secret.py`

* To build the web app, run `python3 server.py`

* Use the web app to first authorize your master account, and then any other Spotify user will be able to use this app by entering their Spotify username in the web app

* Schedule `hourly.py` to run hourly

* Schedule `daily.py` to run daily
