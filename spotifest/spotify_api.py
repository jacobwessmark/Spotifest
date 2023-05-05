import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os


class CreatePlaylist:
    def __init__(self, bands=None, festival=None):

        load_dotenv()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                                            client_secret=os.getenv("CLIENT_SECRET"),
                                                            redirect_uri="http://example.com",
                                                            scope="playlist-modify-private",
                                                            cache_path="token.txt"))
        self.user_id = self.sp.current_user()["id"]
        self.bands = bands
        self.festival = festival

    def create_playlist(self):
        """Create a playlist for a festival"""

        playlist_description = f"This is a summary of songs from the bands playing at {self.festival}."
        new_playlist = self.sp.user_playlist_create(user=self.user_id,
                                                    name=self.festival,
                                                    public=False,
                                                    collaborative=False,
                                                    description=playlist_description)
        # get the playlist id
        playlist_id = new_playlist["id"]
        print("--------------------------------------------------")
        print(f"Playlist for {self.festival} created successfully!")
        print(f"Playlist ID: {playlist_id}")

        # get the top songs from the bands
        print("--------------------------------------------------")

        for band in self.bands:
            song_uri = self.get_topp_songs(band)
            print(f"Adding songs to the {self.festival} playlist")
            self.sp.playlist_add_items(playlist_id=playlist_id, items=song_uri)

        return playlist_id

    def get_topp_songs(self, band):
        """Get the 2 top songs from an artist"""
        # get the artist id
        try:
            if band.lower()[:4] == "and ":
                band = band[4:]
            print(f"searching for {band}...")
            artist_id = self.sp.search(q=f"artist:{band}", type="artist")["artists"]["items"][0]["id"]
            top_tracks = self.sp.artist_top_tracks(artist_id)["tracks"][:2]
            # get the song uris
            song_uris = [song["uri"] for song in top_tracks]

        except IndexError:
            print(f"Couldn't find {band} in Spotify.")

        else:
            return song_uris
