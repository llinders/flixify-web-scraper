import logging

import scrapy.signals
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http.request.form import FormRequest
from scrapy.utils.project import get_project_settings

from flixify.dataaccess.db_statements import insert_movie
from flixify.lib.functions import parse_movie_json, parse_cookie, parse_movie_info

logging.getLogger('scrapy').propagate = False


class FlixifyScraper(scrapy.Spider):
    name = 'FlixifyScraper'
    start_urls = ["https://flixify.com"]
    allowed_domains = ["flixify.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pxid = ""
        self.auid = ""
        self.pip = ""
        self.session = ""

    def start_requests(self):
        form_request = [FormRequest("https://flixify.com/login",
                                    formdata={'email': 'keesdekabouter12+1234@gmail.com',
                                              'password': 'PythonTest'},
                                    callback=self.after_login)]
        return form_request

    def after_login(self, response):
        # Check login succeed before going on
        body = response.body
        if b"The email address or password you entered is not valid" in body:
            logging.error("Login failed")
            return
        else:
            # Login successful
            cookies = response.headers.getlist(b'Set-Cookie')
            self.pxid = parse_cookie(cookies[0])
            self.auid = parse_cookie(cookies[1])
            self.pip = parse_cookie(cookies[2])
            self.session = parse_cookie(cookies[3])
            for page in range(1, 245):
                logging.info(page)
                request = Request(
                    url="https://flixify.com/movies?_t=p1bh7n&_u=hc6rzsskfl&add_mroot=1&description=1&o=c&"
                        "p={0}&postersize=poster&previewsizes=%7B%22preview_list%22:%22big3-index%22,"
                        "%22preview_grid%22:%22video-block%22%7D&slug=1&type=movies".format(page),
                    headers={'Accept': 'application/json'}, callback=self.handle_movies)
                request.cookies['pxid'] = self.pxid
                request.cookies['auid'] = self.auid
                request.cookies['pip'] = self.pip
                request.cookies['session'] = self.session
                yield request

    @staticmethod
    def handle_movies(response):
        json_parsed = parse_movie_json(response.body)
        insert_movie(json_parsed['item']['id'], json_parsed['item']['title'], json_parsed['item']['description'],
                     json_parsed['item']['year'], json_parsed['item']['lang'], json_parsed['item']['genres'],
                     json_parsed['item']['media'], json_parsed['item']['subtitles'])
        for item in json_parsed['items']:
            yield Request(
                url=(
                    "https://flixify.com{0}?_t=olusmk&add_mroot=1&cast=0&crew=0&description=1&episodes_list=1"
                    "&postersize=poster&previewsizes=%7B%22preview_grid%22:%22video-block%22,"
                    "%22preview_list%22:%22big3-index%22%7D&season_list=1&slug=1&sub=1").format(item['url']),
                headers={'Accept': 'application/json'}, callback=parse_movie_info)


process = CrawlerProcess(get_project_settings())
process.crawl(FlixifyScraper)
process.start()  # the script will block here until the crawling is finished
