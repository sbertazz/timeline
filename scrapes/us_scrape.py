from scrapes.classes.scrapers import WikiScraper

UsWiki = WikiScraper(url='https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States')
tables = UsWiki.scrape_tables(tables_to_keep=[1])
UsWiki.parse_tables_us()
UsWiki.save_tables('us_presidents')
print(1)
