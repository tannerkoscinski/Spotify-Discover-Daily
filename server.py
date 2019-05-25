"""This script builds the Flask app."""
import pandas
from flask import Flask, request, render_template, redirect
from spotipy.client import SpotifyException
import spotipy.oauth2 as oauth2
from functions import initializer, history, remover, toptracksartists
from functions import discovery, releaser, follower, playlist, includer
from functions import authorize, logger
from secret import SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def flask_app():
    """This function builds the Flask app."""
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/submission', methods=['POST'])
    def submission():
        username = request.form['username']
        try:
            logger(username, 'submit attempt')
            spotify_object = initializer(username)
            history(username, spotify_object)
            remover(username)
            discovery(username, spotify_object)
            follower(username, spotify_object)
            playlist(username)
            logger(username, 'submit success')
            return render_template('success.html')
        except SpotifyException:
            logger(username, 'authorize request')
            sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,
                                           REDIRECT_URI, scope=SCOPE)
            return redirect(sp_oauth.get_authorize_url())

    @app.route('/authorization', methods=['GET'])
    def authorization():
        username = pandas.read_csv('log.csv')
        username = username.loc[username['event'] == 'authorize request',
                                'username'].reset_index(drop=True)[0]
        response = request.url
        try:
            logger(username, 'authorize attempt')
            authorize(username, response)
            spotify_object = initializer(username)
            history(username, spotify_object)
            toptracksartists(username, spotify_object)
            discovery(username, spotify_object)
            releaser(username, spotify_object)
            follower(username, spotify_object)
            playlist(username)
            includer(username)
            logger(username, 'authorize success')
            return render_template('success.html')
        except SpotifyException:
            return render_template('error.html')

    return app


if __name__ == '__main__':
    APP = flask_app()
    APP.run(debug=True, host='0.0.0.0')
