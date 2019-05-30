"""This script contains all of the functions."""
import datetime
import pandas
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from secret import SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, MASTER


def initializer(username, scope=SCOPE, client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI):
    """This function creates the spotify_object."""
    token = util.prompt_for_user_token(username, scope, client_id,
                                       client_secret, redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object


def history(username, spotify_object):
    """This function saves the play history."""
    recent = spotify_object.current_user_recently_played()['items']
    try:
        data = pandas.read_csv(username + '_history.csv')
        last = data.iloc[len(data) - 1, 0]
    except IOError:
        data = pandas.DataFrame()
        last = '0'
    newdata = pandas.DataFrame()
    for i in recent:
        if i['played_at'] > last:
            row = pandas.DataFrame([[i['played_at'], i['track']['name'],
                                     i['track']['id'],
                                     i['track']['artists'][0]['name'],
                                     i['track']['artists'][0]['id'],
                                     i['track']['album']['name'],
                                     i['track']['album']['id']]],
                                   columns=['playedat', 'track', 'trackid',
                                            'artist', 'artistid', 'album',
                                            'albumid'])
            newdata = row.append(newdata)
    data = data.append(newdata)
    data.to_csv(username + '_history.csv', index=False)


def remover(username):
    """This function removes tracks from the Discovery playlist."""
    account = initializer(MASTER)
    dplaylist = pandas.read_csv(username + '_playlists.csv')['playlistid'][3]
    newtracks = account.user_playlist_tracks(MASTER, dplaylist)
    if newtracks['total'] > 0:
        try:
            tracks = pandas.read_csv(username + '_remover.csv')
        except IOError:
            tracks = pandas.DataFrame()
        while True:
            for i in newtracks['items']:
                row = pandas.DataFrame([[i['added_at'], i['track']['name'],
                                         i['track']['id'],
                                         i['track']['artists'][0]['name'],
                                         i['track']['artists'][0]['id'],
                                         i['track']['album']['name'],
                                         i['track']['album']['id']]],
                                       columns=['playedat', 'track', 'trackid',
                                                'artist', 'artistid', 'album',
                                                'albumid'])
                tracks = tracks.append(row)
            if newtracks['next']:
                newtracks = account.next(newtracks)
            else:
                break
        tracks.to_csv(username + '_remover.csv', index=False)
        account.user_playlist_replace_tracks(MASTER, dplaylist, [])


def toptracksartists(username, spotify_object):
    """This function saves the top tracks and top artists."""
    data = pandas.DataFrame()
    for i in ['short_term', 'medium_term']:
        toptracks = spotify_object.current_user_top_tracks(
            limit=50, time_range=i)['items']
        for j in toptracks:
            row = pandas.DataFrame([[j['name'], j['id'],
                                     j['artists'][0]['name'],
                                     j['artists'][0]['id'], j['album']['name'],
                                     j['album']['id']]],
                                   columns=['track', 'trackid', 'artist',
                                            'artistid', 'album', 'albumid'])
            data = data.append(row)
    data = data.drop_duplicates()
    data.to_csv(username + '_top_tracks.csv', index=False)
    data = pandas.DataFrame()
    for i in ['short_term', 'medium_term']:
        topartists = spotify_object.current_user_top_artists(
            limit=50, time_range=i)['items']
        for j in topartists:
            row = pandas.DataFrame([[j['name'], j['id']]],
                                   columns=['artist', 'artistid'])
            data = data.append(row)
    data = data.drop_duplicates()
    data.to_csv(username + '_top_artists.csv', index=False)


def discovery(username, spotify_object):
    """This function saves the discovery tracks."""
    playlists = spotify_object.current_user_playlists()['items']
    sources = pandas.DataFrame()
    for i in playlists:
        row = pandas.DataFrame([[i['name'], i['id'], i['owner']['id']]],
                               columns=['playlist', 'playlistid', 'ownerid'])
        if i['owner']['id'] == 'spotify':
            if i['name'] == 'Discover Weekly':
                sources = row.append(sources)
            else:
                sources = sources.append(row)
    data = pandas.DataFrame(columns=['trackid', 'track', 'artist', 'album',
                                     'playlist'])
    if not sources.empty:
        for i, j in enumerate(sources['playlistid']):
            tracks = spotify_object.user_playlist_tracks(
                sources['ownerid'].iloc[i], j)['items']
            for k in tracks:
                if k['track']:
                    row = pandas.DataFrame([[k['track']['id'],
                                             k['track']['name'],
                                             k['track']['artists'][0]['name'],
                                             k['track']['album']['name'],
                                             sources['playlist'].iloc[i]]],
                                           columns=['trackid', 'track',
                                                    'artist', 'album',
                                                    'playlist'])
                    data = data.append(row)
        played = pandas.read_csv(username + '_history.csv',
                                 usecols=['track', 'artist']).drop_duplicates()
        try:
            remove = pandas.read_csv(username + '_remover.csv',
                                     usecols=['track', 'artist'])
        except IOError:
            remove = pandas.DataFrame()
        if not remove.empty:
            played = played.append(remove).drop_duplicates()
        drop = len(played)
        data = played.append(data, sort=False).drop_duplicates(
            subset=['track', 'artist'])
        data = data.iloc[drop:]
    data.to_csv(username + '_discovery.csv', index=False)


def releaser(username, spotify_object):
    """This function saves the releaser tracks."""
    artists = pandas.read_csv(username + '_top_artists.csv')
    newalbums = pandas.DataFrame()
    for i in artists['artistid']:
        albums = spotify_object.artist_albums(i, album_type='album,single',
                                              limit=50)['items']
        for j in albums:
            if j['release_date'] > str(datetime.date.today()
                                       - datetime.timedelta(days=28)):
                row = pandas.DataFrame([[j['id'], j['release_date'], j['name'],
                                         j['artists'][0]['name']]],
                                       columns=['albumid', 'release_date',
                                                'album', 'artist'])
                newalbums = newalbums.append(row)
    newalbums = newalbums.sort_values(by='release_date',
                                      ascending=False).iloc[0:20]
    albums = spotify_object.albums(newalbums['albumid'])['albums']
    data = pandas.DataFrame()
    for i in albums:
        for j in i['tracks']['items']:
            row = pandas.DataFrame([[j['id'], j['name'], i['name'],
                                     i['artists'][0]['name'],
                                     i['release_date']]],
                                   columns=['trackid', 'track', 'album',
                                            'artist', 'release'])
            data = data.append(row)
    data.to_csv(username + '_releaser.csv', index=False)


def follower(username, spotify_object):
    """This function creates and follows the playlists."""
    try:
        playlists = pandas.read_csv(username + '_playlists.csv')
    except IOError:
        playlists = pandas.DataFrame()
    if playlists.empty:
        account = initializer(MASTER)
        titles = ['Top Tracks', 'Discovery', 'Releaser', 'Remover']
        descriptions = ['Your top 50 tracks from the last 4 weeks combined '
                        'with your top 50 tracks from the last 6 months.',
                        'The songs you haven\'t listened to from the Spotify '
                        'playlists you follow.',
                        'All the new releases from your top artists.',
                        'Add songs here to remove them from your Discovery '
                        'playlist.']
        for i in range(3, -1, -1):
            account.user_playlist_create(MASTER, titles[i], public=False,
                                         description=descriptions[i])
        newplaylists = account.user_playlists(MASTER, limit=4)['items']
        account.user_playlist_change_details(MASTER, newplaylists[3]['id'],
                                             collaborative=True)
        for i in newplaylists:
            row = pandas.DataFrame([[i['name'], i['id']]],
                                   columns=['playlist', 'playlistid'])
            playlists = playlists.append(row)
        playlists.to_csv(username + '_playlists.csv', index=False)
    for i in playlists['playlistid'][::-1]:
        if not spotify_object.user_playlist_is_following(MASTER, i,
                                                         [username])[0]:
            spotify_object.user_playlist_follow_playlist(MASTER, i)


def playlist(username):
    """This function adds the tracks to the playlists."""
    playlists = pandas.read_csv(username + '_playlists.csv')
    account = initializer(MASTER)
    tracks = pandas.read_csv(username + '_top_tracks.csv')['trackid']
    account.user_playlist_replace_tracks(MASTER, playlists['playlistid'][0],
                                         tracks)
    tracks = pandas.read_csv(username + '_discovery.csv')['trackid']
    account.user_playlist_replace_tracks(MASTER, playlists['playlistid'][1],
                                         tracks[:100])
    if len(tracks) > 100:
        account.user_playlist_add_tracks(MASTER, playlists['playlistid'][1],
                                         tracks[100:200])
    tracks = pandas.read_csv(username + '_releaser.csv')['trackid'][:100]
    account.user_playlist_replace_tracks(MASTER, playlists['playlistid'][2],
                                         tracks)


def includer(username):
    """This function includes the user."""
    users = pandas.read_csv('usernames.csv')
    if username not in list(users['username']):
        row = pandas.DataFrame([[username]], columns=['username'])
        users = users.append(row)
        users.to_csv('usernames.csv', index=False)


def excluder(username):
    """This function excludes the user."""
    users = pandas.read_csv('usernames.csv')
    users = users[users['username'] != username]
    users.to_csv('usernames.csv', index=False)


def authorize(response, scope=SCOPE, client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI):
    """This function authorizes the user."""
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope, cache_path='.cache-temp')
    code = sp_oauth.parse_response_code(response)
    sp_oauth.get_access_token(code)
    token = util.prompt_for_user_token('temp', scope, client_id,
                                       client_secret, redirect_uri)
    spotify_object = spotipy.Spotify(auth=token)
    username = spotify_object.current_user()['id']
    open('.cache-' + username, 'w').write(open('.cache-temp', 'r').read())
    return username


def logger(username, event):
    """This function logs attempts."""
    log = pandas.read_csv('log.csv')
    row = pandas.DataFrame([[datetime.datetime.now(), username, event]],
                           columns=['datetime', 'username', 'event'])
    log = row.append(log)
    log.to_csv('log.csv', index=False)
