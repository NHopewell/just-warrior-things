from typing import List, Tuple, Optional

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

            self.data.append(tuple([title, link]))

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

            self.data.append(tuple([title, link]))

        return self.data




if __name__ == '__main__':
    
    '''
    URL = 'https://www.icy-veins.com/forums/search/?q=warrior&type=forums_topic&updated_after=any&sortby=newest&search_and_or=or&search_in=titles'
    icy = IcyVeinsScrapper(URL)
    scraped_icy_veins_data = icy.scrape()

    print(scraped_icy_veins_data)
    '''

    URL = "https://www.mmo-champion.com/forums/278-Warrior?sort=lastpost&order=desc"
    mmo = MMOChampionScrapper(URL)
    mmo_data = mmo.scrape()
    
    print(mmo_data)