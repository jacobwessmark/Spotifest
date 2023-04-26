import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from songkick_scrap import FestivalScraper
from pprint import pprint
import os




class CreatePlaylist:
    def __init__(self, bands, festival):

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

        playlist_description = f"This is a summry of songs from the bands playing at {festival_name}."

        new_playlist = self.sp.user_playlist_create(user=self.user_id,
                                                    name=self.festival,
                                                    public=True,
                                                    collaborative=False,
                                                    description=playlist_description)
        # get the playlist id
        playlist_id = new_playlist["id"]
        print("--------------------------------------------------")
        print(f"Playlist for {festival_name} created successfully!")
        print(f"Playlist ID: {playlist_id}")

        # get the top songs from the bands
        print("--------------------------------------------------")

        for band in self.bands:
            song_uri = self.get_topp_songs(band)
            print(f"Adding songs to the {festival_name} playlist")
            self.sp.playlist_add_items(playlist_id=playlist_id, items=song_uri)

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


# if __name__ == "__main__":
#     new_playlist = CreatePlaylist(festival="Subkultfestival", bands=["Hammerfall", "Kanye West", "Celine Dion"])
#     playlist_url = new_playlist.create_playlist()
#     print(playlist_url)