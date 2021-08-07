from scrapes.classes.scrapers import WikiScraper

ItaWiki = WikiScraper(url='https://en.wikipedia.org/wiki/List_of_prime_ministers_of_Italy')
tables = ItaWiki.scrape_tables()
ItaWiki.parse_tables_it()
ItaWiki.save_tables('ita_pm')
print(1)
