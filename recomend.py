import pandas as pd
import pickle
import requests

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('clean_genres.csv', index_col=0)
q_df = df.drop(columns=['uri'])

CLIENT_ID = 'ffd61f80a4dd4d7c8fc0c289d994fec0'
CLIENT_SECRET = '4d2e3a2dc89c45be83eaa5083b9b1b48'


def get_nn_query(track_id):
    """Get spotify request for song audio-features, format it for query_nn()."""
    # get access token
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']

    # GET song audio-features
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    r = requests.get('https://api.spotify.com/v1/audio-features/' + track_id, headers=headers)
    song_dict = r.json()

    # put audio attributes in same order as in the dataframe the estimator is fit to.
    query_nn = [song_dict[x] for x in q_df.columns]

    return query_nn


def query_nn_pickles(song_features):
    """Load pickles, scale song_features, return 5 nearest neighbors."""
    # load pkls from current directory
    sclr = pickle.load(open('sclr.pkl', 'rb'))
    knn = pickle.load(open('knn.pkl', 'rb'))
    # scale features
    scaled = sclr.transform([song_features])
    print(scaled)
    # get 5 nearest neighbors, returns a list of dataframe indices
    similar_five = knn.kneighbors(scaled, 5, return_distance=False)

    return similar_five


def recomend(song_link):
    """Take song_link, return 5 similar songs from dataframe."""
    # Slice uri out of spotify share link
    uri = song_link[31:53]
    # Request song audio-features and format them for nearest-neighbors query
    features = get_nn_query(uri)
    # get nearest neighbors
    similar_songs = query_nn_pickles(features)

    # create links to spotify songs
    query_results = df.loc[similar_songs[0]]['uri']
    links = query_results.apply(
        lambda x: 'https://open.spotify.com/track/' + x[14:]).values

    return links
