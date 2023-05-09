import bs4
import requests
from sqlalchemy.exc import IntegrityError
from spotifest import app, db
from spotifest.models import FestivalBand, Festival, Band
from flask import jsonify


class FestivalCreator:
    """This class is used to scrape festivals from songkick.com or manually add them to the database"""
    def __init__(self, country=None):
        self.country_code = country

    def scrape_festivals_from_web(self):
        """This method scrapes festivals from songkick.com and adds them to the database"""

        # Vi använder oss av app.app_context() för att kunna använda oss av SQLAlchemy
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
                self.add_band_to_db(festival_dict)

    @staticmethod
    def add_band_to_db(festival_dict):
        """This method adds bands to the database, there needs to be a festival in the database in order
        to make the festival_band relation, so make sure you've added the festival before calling this method"""
        for band in festival_dict["bands"]:

            if band.lower()[:4] == "and ":
                band = band[4:]
            band_db = Band(name=band)
            try:
                db.session.add(band_db)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()  # Roll back the transaction
                print(f"{band} already in database. ")

            festival_band = FestivalBand(festival_name=festival_dict["name"], band_name=band)
            db.session.add(festival_band)
            db.session.commit()
        return {"band_result": f"Added {festival_dict['bands']} to database successfully"}

    @staticmethod
    def add_festival_to_db(festival_dict):
        """This method adds festivals to the database"""
        festival_db = Festival(date=festival_dict["date"],
                               name=festival_dict["name"],
                               venue=festival_dict["venue"],
                               country=festival_dict["country"]
                               )
        try:
            db.session.add(festival_db)
            db.session.commit()
            return {"festival_result": f"Added {festival_dict['name']} to database successfully"}

        except IntegrityError:
            db.session.rollback()  # Roll back the transaction
            return {"error": f"{festival_dict['name']} already in database :"}

