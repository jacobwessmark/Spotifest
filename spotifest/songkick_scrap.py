import bs4
import requests

# TODO: Vart ska denna filen ligga? I en egen mapp? I en egen app? I en egen app i en egen mapp?

class FestivalScraper:
    def __init__(self, country):
        self.festival_list = []
        self.country_code = country

        self.add_festivals_to_list()

    def add_festivals_to_list(self):
        # Get the HTML from the page
        res = requests.get(f'https://www.songkick.com/festivals/countries/{self.country_code}')

        # Parse the HTML
        soup = bs4.BeautifulSoup(res.content, 'html.parser')

        # get the list of festivals
        div_element = soup.find(id="event-listings")

        # print the list of festivals
        festival_divs = div_element.find_all('li', title=True)

        for festival in festival_divs:
            festival_dict = {
                "date": festival["title"],
                "name": festival.find("p", class_="artists summary").find("a").find("strong").get_text(strip=True)[:-5],
                "location": festival.find('p', class_='location').get_text(strip=True),
                "bands": festival.find("p", class_="artists summary").find("a").find("span").get_text(strip=True).split(
                    ", ")
            }
            self.festival_list.append(festival_dict)

    def get_festivals(self):
        return self.festival_list
