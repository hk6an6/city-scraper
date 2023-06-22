import scrapy
from dataclasses import dataclass

@dataclass
class RestaurantItem:
  """Represents a restaurant in TripAdvisor"""  
  name: str
  stars: str
  url: str


def bubblesToScore(bubbles):
  """Takes TripAdvisor's "bubbles" and returns a rating

  Args:
      bubbles (str): the "aria-label" for the svg that
      represents ratings in TripAdvisor.

  Returns:
      str: a value from 1 to 5 rating a restaurant
  """  
  # Restaurant ratings look like "5 out of 5"
  values = bubbles.split(' ')
  # pick the first number as the rating
  return values[0]


class CitySpider(scrapy.Spider):
  """Retrieves restaurants from a city in TripAdvisor"""  
  name = 'CitySpider'
  start_urls = ['https://www.tripadvisor.com/Restaurants-g315917-Nerja_Costa_del_Sol_Province_of_Malaga_Andalucia.html']
  custom_settings = {
        "USER_AGENT": f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

  def parse(self, response):
    """parses a city in TripAdvisor

    Args:
        response (scrapy.http.Response): contains the response from the website.

    Yields:
        RestaurantItem: Restaurants extracted from TripAdvisor
    """    
    # find boxes with restaurants
    for div in response.css('div.QEXGj'):
      # find links to the restaurant page
      anchorSelector = div.css('a.Lwqic.Cj.b')
      # skip if no link found
      if(not anchorSelector):
        continue
      # find the image with restaurant ratings
      svgSelector = div.css('svg.UctUV.d.H0')
      # skip if no ratings found
      if(not svgSelector):
        continue
      # find the text for the restaurant's name
      titleSelector = anchorSelector.xpath("text()[3]") \
        or anchorSelector.xpath("text()")
      # find the text for the restaurant's rating
      bubbles = bubblesToScore(svgSelector.attrib["aria-label"])
      # store restaurant information
      restaurant_item = RestaurantItem(
        name=titleSelector.get()
        ,stars=bubbles
        ,url=anchorSelector.attrib["href"])
      print(f'{restaurant_item.name}, {restaurant_item.stars}')
      yield restaurant_item
