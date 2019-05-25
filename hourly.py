"""This script runs hourly."""
import pandas
from spotipy.client import SpotifyException
from functions import initializer, history, excluder, logger
for user in pandas.read_csv('usernames.csv')['username']:
    try:
        spotifyobject = initializer(user)
        history(user, spotifyobject)
        logger(user, 'hourly')
    except SpotifyException:
        excluder(user)
        logger(user, 'remove')
