"""This script contains the secret variables."""
SCOPE = 'user-read-recently-played user-top-read user-library-modify ' \
        'user-library-read playlist-read-private playlist-modify-public ' \
        'user-read-email user-read-birthdate user-read-private ' \
        'user-read-playback-state user-modify-playback-state ' \
        'user-read-currently-playing app-remote-control streaming ' \
        'user-follow-read user-follow-modify'
CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
REDIRECT_URI = 'http://0.0.0.0:5000/authorization'
MASTER = 'YOUR_SPOTIFY_MASTER_USERNAME'
