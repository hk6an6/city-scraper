import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dataclasses import dataclass
import base64
import re

@dataclass
class RestaurantItem:
  """Represents a restaurant in TripAdvisor"""  
  name: str
  stars: str
  url: str
  food: str
  service: str
  value: str
  cuisines: str
  address: str
  maps: str
  phone: str

class RestaurantSpider(CrawlSpider):
  name = "tripadvisor"
  allowed_domains = ["tripadvisor.com"]
  start_urls = ["https://www.tripadvisor.com/Restaurants-g315917-Nerja_Costa_del_Sol_Province_of_Malaga_Andalucia.html"]
  custom_settings = {
        "USER_AGENT": f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        , "AUTOTHROTTLE_ENABLED" : True

    }
  
  rules = (
    Rule(LinkExtractor(
      allow=(r"Restaurant_Review-"),
      restrict_css=('div.QEXGj a'),
    ), callback="parse_restaurant"
    , follow=True)
    , Rule(LinkExtractor(
      restrict_xpaths=('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div')
    ))
  )

  def class_to_rating(self, class_name):
    if (not class_name):
      return "NA"
    score = float(class_name.split('_')[-1])
    return score / 10
  
  def decodebase64(self, coded_string):
    if (not coded_string):
      return "NA"
    decoded = base64.b64decode(coded_string)
    return decoded[4:-4]
  
  def extract_cuisines(self, response):
    money = re.compile(r'\$\d+')
    cuisines = response.xpath('//*/div/div/div/div/div/div[@data-tab="TABS_DETAILS"]/div/div/div/div/div/div/div[@class="AGRBq"]')
    if (len(cuisines) >= 3):
      return cuisines[3].css('::text').get()
    cuisines = response.xpath('//*/div[@class="SrqKb"]/text()').get()
    if (not money.match(cuisines)):
      return cuisines
    return response.xpath('//*/div[@class="SrqKb"]/text()')[1].get()
    

  def parse_restaurant(self, response):
    return RestaurantItem(
      name=response.xpath('//*/h1[1]/text()').get()
      , stars=response.css('div.QEQvp > span.ZDEqb::text')[0].get()
      , url=response.url
      , food=self.class_to_rating(
        response.xpath('//*/div/div/div[1]/div/div[3]/div[2]/div[1]/span[3]/span').css('::attr(class)').get()
      )
      , service=self.class_to_rating(
        response.xpath('//*/div/div/div[1]/div/div[3]/div[2]/div[2]/span[3]/span').css('::attr(class)').get()
      )
      , value=self.class_to_rating(
        response.xpath('//*/div/div/div[1]/div/div[3]/div[2]/div[3]/span[3]/span').css('::attr(class)').get()
      )
      , cuisines=self.extract_cuisines(response)
      , address=response.css('div> span > a > span.yEWoV::text').get()
      , maps=self.decodebase64(
        response.css('div> span > a.YnKZo.Ci.Wc._S.C.FPPgD::attr(data-encoded-url)')[0].get()
      )
      , phone=response.css('div.f > div.IdiaP.Me > a::attr(href)')[0].get()
    )
