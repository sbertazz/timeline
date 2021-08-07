from scrapes.classes.scrapers import WikiScraper

UkWiki = WikiScraper(url='https://en.wikipedia.org/wiki/List_of_prime_ministers_of_the_United_Kingdom')
tables = UkWiki.scrape_tables(tables_to_keep=[1])
UkWiki.parse_tables_uk()
UkWiki.save_tables('uk_pm')
print(1)
