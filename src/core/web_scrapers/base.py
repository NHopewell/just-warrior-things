import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

import requests
from bs4 import BeautifulSoup



class Scraper(ABC):
    """
    abstract class acting as our web scrapper class template
    """

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        """
        :param url: A complete url to scrape (incluing query parameters).
        :param parser_type: Which bs4 parser to use. Default = html.parser
        """
        self.url = url
        self.parser_type = parser_type
        self.page = None
        self.soup = None
        self.data = []

    def _bind_soup(self) -> None:
        """
        Binds the resulting data from a requests call on the url passed to
        the scraper and uses the page to bind the html bs4 content.
        """
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, self.parser_type)
    
    @staticmethod
    def _parse_date(
        date: str,
        input_format: str,
        output_format: Optional[str] = '%Y-%m-%d %H:%M') -> str:
        """
        Converts a string representing a date in a format specified by the user
        to a new date string in the desired output format.
        """

        return datetime.datetime.strptime(date, input_format).strftime(output_format)

    @staticmethod
    def _convert_to_military_time(
        date: str,
        input_format: str,
        output_format: Optional[str] = '%Y-%m-%d %H:%M') -> str:
        """
        Converts a 12 hour clock time to 24 hour military time.
        """

        date = datetime.datetime.strptime(date, input_format)
        date_in_military_time = date + datetime.timedelta(hours=12)

        return date_in_military_time.strftime(output_format)

    @abstractmethod
    def scrape(self)-> List[Tuple[str]]:
        """
        Scrape the bound URL. 
        
        This method must be overridden in every child class.
        The logic of how each child class will scrape their bound URL will be different
        depending on the structure of the HTML of the page scraped.
        """
        pass