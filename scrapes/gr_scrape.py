from scrapes.classes.scrapers import WikiScraper

"""  NOT IMPLEMENTED """
GrWiki = WikiScraper(url='https://en.wikipedia.org/wiki/List_of_prime_ministers_of_Greece')
tables = GrWiki.scrape_tables(tables_to_keep=[2, 3, 4, 5, 6, 7])
GrWiki.parse_tables()
# GrWiki.save_tables(['ita_monarchy', 'ita_republic'])
print(1)
