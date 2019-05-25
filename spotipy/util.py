from __future__ import print_function
from . import oauth2


def prompt_for_user_token(username, scope=None, client_id=None,
                          client_secret=None, redirect_uri=None,
                          cache_path=None):

    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope, cache_path=cache_path)

    token_info = sp_oauth.get_cached_token()

    if token_info:
        return token_info['access_token']
    else:
        return None
