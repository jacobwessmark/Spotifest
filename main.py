from datebase_control import DatabaseControl
from songkick_scrap import FestivalScraper


if __name__ == "__main__":

    festival_scraper = FestivalScraper("US")
    festival_list = festival_scraper.get_festivals()
    new_connect = DatabaseControl()
    new_connect.add_festivals_to_database(festival_list)

    # TODO: Get data from database and make a playlist.
