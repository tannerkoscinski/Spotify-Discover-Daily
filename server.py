"""This script builds the Flask app."""
import pandas
from flask import Flask, request, render_template, redirect
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

    @app.route('/click', methods=['GET'])
    def click():
        logger('button', 'click')
        sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET,
                                       REDIRECT_URI, scope=SCOPE)
        return redirect(sp_oauth.get_authorize_url())

    @app.route('/authorization', methods=['GET'])
    def authorization():
        response = request.url
        username = authorize(response)
        usernames = pandas.read_csv('usernames.csv')
        logger(username, 'attempt')
        spotify_object = initializer(username)
        history(username, spotify_object)
        if username in list(usernames['username']):
            remover(username)
            discovery(username, spotify_object)
            follower(username, spotify_object)
            playlist(username)
        else:
            toptracksartists(username, spotify_object)
            discovery(username, spotify_object)
            releaser(username, spotify_object)
            follower(username, spotify_object)
            playlist(username)
            includer(username)
        logger(username, 'success')
        return render_template('success.html')

    return app


if __name__ == '__main__':
    APP = flask_app()
    APP.run(debug=True, host='0.0.0.0')
