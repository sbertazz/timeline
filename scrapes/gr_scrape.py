from scrapes.classes.scrapers import WikiScraper

"""  NOT IMPLEMENTED """
GrWiki = WikiScraper(url='https://en.wikipedia.org/wiki/List_of_prime_ministers_of_Greece')
tables = GrWiki.scrape_tables(tables_to_keep=[2, 3, 4, 5, 6, 7])
GrWiki.parse_tables_gr()
GrWiki.save_tables('gr_mp')
print('GR done')
