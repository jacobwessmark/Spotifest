import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from songkick_scrap import FestivalScraper
from pprint import pprint
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class CreatePlaylist:
    def __init__(self, country):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                            client_secret=CLIENT_SECRET,
                                                            redirect_uri="http://example.com",
                                                            scope="playlist-modify-private",
                                                            cache_path="token.txt"))
        self.user_id = self.sp.current_user()["id"]
        self.festival_data = self.get_list_of_festivals(country)
        self.create_playlist()


    @staticmethod
    def get_list_of_festivals(country):
        festival_scraper = FestivalScraper(country)
        festival_data = festival_scraper.get_festivals()

        return festival_data

    def create_playlist(self):
        """Create a playlist for a festival"""
        # prompt the user with the festival names
        for festival in self.festival_data:
            print(festival["name"] + " - " + festival["date"])
        print("--------------------------------------------------")

        festival_name = input("Which festival do you want to create a playlist for? ")

        # get the bands playing at the festival
        bands = []
        print(f"searching for bands at {festival_name}...")
        for festival in self.festival_data:
            if festival["name"] == festival_name:
                bands = festival["bands"]
                print(f"Found {len(bands)} bands playing at {festival_name}!")
                break

        print(bands)

        playlist_description = f"This is a summry of songs from the bands playing at {festival_name}."

        new_playlist = self.sp.user_playlist_create(user=self.user_id,
                                                    name=festival_name,
                                                    public=False,
                                                    collaborative=False,
                                                    description=playlist_description)
        # get the playlist id
        playlist_id = new_playlist["id"]
        print("--------------------------------------------------")
        print(f"Playlist for {festival_name} created successfully!")
        print(f"Playlist ID: {playlist_id}")

        # get the top songs from the bands
        print("--------------------------------------------------")

        for band in bands:
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


if __name__ == "__main__":


    festival_playlist = CreatePlaylist("us")
