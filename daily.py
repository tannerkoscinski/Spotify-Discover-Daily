"""This script runs daily."""
import pandas
from spotipy.client import SpotifyException
from functions import initializer, history, remover, toptracksartists
from functions import discovery, releaser, playlist, excluder, logger
for user in pandas.read_csv('usernames.csv')['username']:
    try:
        spotifyobject = initializer(user)
        history(user, spotifyobject)
        remover(user)
        toptracksartists(user, spotifyobject)
        discovery(user, spotifyobject)
        releaser(user, spotifyobject)
        playlist(user)
        logger(user, 'daily')
    except SpotifyException:
        excluder(user)
        logger(user, 'remove')
