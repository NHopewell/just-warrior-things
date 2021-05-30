from typing import List, Tuple, Optional
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from base import Scraper


class IcyVeinsScrapper(Scraper):

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        super().__init__(url, parser_type)

    def scrape(self) -> List[Tuple[str]]:
        """
        Scrape posts from icy veins forums where 'warrior' is includes in title

        https://www.icy-veins.com/forums/search/?q=warrior&type=forums_topic&updated_after=any&sortby=newest&search_and_or=or&search_in=titles
        """

        self._bind_soup()
        results = self.soup.find_all(class_="ipsStreamItem_container")

        for res in results:
            ancor = res.div.div.a

            title = ancor.text
            link = ancor['href'].split("?")[0]
            date_with_suffix = res.ul.li.a.time["title"].split()
            clean_date = self.return_cleaned_date(date_with_suffix, input_format='%m/%d/%Y %H:%M')

            self.data.append(tuple([title, link, clean_date]))

        return self.data


class MMOChampionScrapper(Scraper):

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        super().__init__(url, parser_type)

    def scrape(self) -> List[Tuple[str]]:
        """
        Scrape posts from mmo chamption warrior class forums

        https://www.mmo-champion.com/forums/278-Warrior?sort=lastpost&order=desc
        """

        self._bind_soup()
        results = self.soup.find('ol', id='threads')
        results = results.find_all(class_="threadbit hot")

        for res in results:
            ancor = res.div.div.div.a
            title = ancor.text
            link = "/".join(["https://www.mmo-champion.com", ancor["href"]])

            date_with_suffix = res.div.dl.find_all('dd')[1].text.split(" ")
            clean_date = self.return_cleaned_date(date_with_suffix, input_format='%Y-%m-%d, %H:%M')

            self.data.append(tuple([title, link, clean_date]))

        return self.data



class RedditScraper(Scraper):

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        super().__init__(url, parser_type)
        self.browser = None


    @staticmethod
    def _convert_posted_ago_to_date(posted: str, output_format: Optional[str] = '%Y-%m-%d %H:%M') -> str:
        
        num, time_period, _ = posted.split(" ")
        num = int(num)
        now = datetime.datetime.strptime(datetime.datetime.today().strftime(output_format), output_format)

        if time_period in ('minute', 'minutes'):
            date = now - datetime.timedelta(minutes=num)
        elif time_period in ('hour', 'hours'):
            date = now - datetime.timedelta(hours=num)
        elif time_period in ('day', 'days'):
            date = now - datetime.timedelta(days=num)
        else:
            date = now

        return date.strftime(output_format)


    def _bind_soup(self) -> None:
        """
        overrides base class to bind soup with selenium browser driver instead of requests
        """
        options = webdriver.ChromeOptions()
        options.add_argument(" - incognito")
        options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

        self.browser = webdriver.Chrome(
            executable_path='/Users/nickhopewell/Development/just-warrior-things/src/core/web_scrapers/chromedriver', 
            options=options)

        self.page = self.browser.get(self.url)
        self.soup = BeautifulSoup(self.browser.page_source, self.parser_type)


class RedditWoWScrapper(RedditScraper):

    def __init__(self, url: str, parser_type: Optional[str] = "html.parser") -> None:
        super().__init__(url, parser_type)

    def scrape(self) -> List[Tuple[str]]:
        """
        Scrape posts from /r/wow with titles containing "warrior"

        https://www.reddit.com/r/wow/search/?q=title%3A%22warrior%22&restrict_sr=1&sort=new
        """
 
        self._bind_soup()
        timeout = 10

        try:
            WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='SHORTCUT_FOCUSABLE_DIV']/div[2]/div/div/div/div[2]/div[3]/div[1]/div[3]/div[1]")
                )
            )
        except TimeoutException:
            print("Timed out when page loading")
            self.browser.quit()
        
        results = self.soup.find('div', class_='QBfRw7Rj8UkxybFpX-USO')
        posts = results.find_all('a', class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
        posted_info = results.find_all('div', class_="_3AStxql1mQsrZuUIFP9xSg iaAYGvTNtknkTxuHArCzL")

        for post, posted in zip(posts, posted_info):
            link = "".join(["https://www.reddit.com", post["href"]])
            title = post.div.h3.span.text
            clean_date = self._convert_posted_ago_to_date(posted.find('a', class_="_3jOxDPIQ0KaOWpzvSQo-1s").text)

            self.data.append(tuple([title, link, clean_date]))

        return self.data



class RedditClasssicWoWScrapper(RedditScraper):
    pass



if __name__ == '__main__':
    

    '''
    URL = 'https://www.icy-veins.com/forums/search/?q=warrior&type=forums_topic&updated_after=any&sortby=newest&search_and_or=or&search_in=titles'
    icy = IcyVeinsScrapper(URL)
    scraped_icy_veins_data = icy.scrape()

    print(scraped_icy_veins_data)
    '''

    
 
    '''
    URL = "https://www.mmo-champion.com/forums/278-Warrior?sort=lastpost&order=desc"
    mmo = MMOChampionScrapper(URL)
    mmo_data = mmo.scrape()
    print(mmo_data)
    '''

    
    URL = 'https://www.reddit.com/r/wow/search/?q=title%3A%22warrior%22&restrict_sr=1&sort=new'

    redditwow = RedditWoWScrapper(URL)
    rdata = redditwow.scrape()

    print(rdata)
  

    

