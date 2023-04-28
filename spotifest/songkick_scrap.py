import bs4
import requests
from sqlalchemy.exc import IntegrityError

from spotifest import app, db
from spotifest.columns import FestivalBand, Festival, Band




class FestivalScraper:
    def __init__(self, country=None):
        self.festival_list = []
        self.country_code = country

    def add_festivals_to_list(self):
        with app.app_context():
            # Get the HTML from the page
            res = requests.get(f'https://www.songkick.com/festivals/countries/{self.country_code}')

            # Parse the HTML
            soup = bs4.BeautifulSoup(res.content, 'html.parser')

            # get the list of festivals
            div_element = soup.find(id="event-listings")

            # print the list of festivals
            festival_divs = div_element.find_all('li', title=True)

            for festival in festival_divs:

                # First we put all the data from scrape to a dict
                festival_dict = {
                    "date": festival["title"],
                    "name": festival.find("p", class_="artists summary").find("a").find("strong").get_text(strip=True)[
                            :-5],
                    "venue": festival.find('p', class_='location').get_text(strip=True),
                    "country": self.country_code,
                    "bands": festival.find("p", class_="artists summary").find("a").find("span").get_text(
                        strip=True).split(", ")
                }

                self.add_festival_to_db(festival_dict)

                for band in festival_dict["bands"]:
                    self.add_band_to_db(band)


    def get_festivals(self):
        return self.festival_list

    @staticmethod
    def add_band_to_db(festival_dict):
        try:
            for band in festival_dict["bands"]:

                if band.lower()[:4] == "and ":
                    band = band[4:]
                band_db = Band(name=band)
                db.session.add(band_db)
                db.session.commit()
                festival_band = FestivalBand(festival_name=festival_dict["name"], band_name=band)
                db.session.add(festival_band)
                db.session.commit()

        except IntegrityError:
            db.session.rollback()  # Roll back the transaction
            print(f"{band} already in database :)")

    def add_festival_to_db(self, festival_dict):
        festival_db = Festival(date=festival_dict["date"],
                               name=festival_dict["name"],
                               venue=festival_dict["venue"],
                               country=festival_dict["country"]
                               )
        db.session.add(festival_db)
        return festival_db
