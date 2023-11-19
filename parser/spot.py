import spotipy
from spotipy.oauth2 import SpotifyOAuth


def spotify_search(query):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="fa1d1b04eea145398e462c21a8dfdb12",
                                                   client_secret="5a8657db4a674f8cb2c5cccdc1ee3462",
                                                   redirect_uri="http://localhost:8080",
                                                   scope="user-library-read"))

    results = sp.search(q=query, type='track')
    tracks = []
    for track in results['tracks']['items']:
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['preview_url']
        })

    return tracks


if __name__ == "__main__":
    search_query = input("Qidirayotgan musiqa: ")
    search_results = spotify_search(search_query)

    print(f"{len(search_results)} ta natija topildi:")
    for idx, track in enumerate(search_results):
        print(f"{idx + 1}: {track['name']} by {track['artist']} - Spotify URL: {track['url']}")
