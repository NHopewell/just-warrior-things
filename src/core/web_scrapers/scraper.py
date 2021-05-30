from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

import requests
from bs4 import BeautifulSoup



class Scraper(ABC):
    """
    abstract class acting as our web scrapper class template
    """

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        self.url = url
        self.parser_type = parser_type
        self.page = None
        self.soup = None
        self.data = []

    def _bind_soup(self) -> None:
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, self.parser_type)

    @abstractmethod
    def scrape(self)-> List[Tuple[str]]:
        pass