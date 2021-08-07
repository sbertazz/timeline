import pandas as pd
import datetime as dt
import pickle
from config import store_location

months_choice = [dt.date(2020,m,1).strftime('%B') for m in range(1,13)]

def from_to_date_parser(rawdatestring):
    try:
        if len(rawdatestring.split(' ')) == 2:
            day, rawmonyear = rawdatestring.split(' ')
        else:
            day, rawmon, rawyear = rawdatestring.split(' ')
            rawmonyear = rawmon + rawyear
        mon = 0
        for n, m in enumerate(months_choice):
            if m in rawmonyear:
                rawyear = rawmonyear.replace(m, '')
                mon = n + 1
        year = int(rawyear[:4])
        final_date = dt.date(year, mon, int(day))
    except Exception as ex:
        print(ex)
        final_date = 'parsing error'
    return final_date



class WikiScraper():
    def __init__(self, url):
        self.url = url
        self.raw_tables = []
        self.parsed_tables = []
        self.parse_errors = []

    def scrape_tables(self):
        # page = requests.get(self.url)
        # soup = BeautifulSoup(page.content, "html.parser")
        # tables = soup.findAll('table')
        tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_prime_ministers_of_Italy')
        self.raw_tables = tables

    def parse_tables(self):
        for raw_table in self.raw_tables:
            parsed_table = raw_table.copy()
            parsed_table[('parsed', 'from')
            ] = parsed_table[('Term of office',     'Took office')].apply(from_to_date_parser)
            parsed_table[('parsed', 'to')
            ] = parsed_table[('Term of office', 'Left office')].apply(from_to_date_parser)
            self.parse_errors.append(parsed_table[(parsed_table['parsed', 'to'] =='parse error') | (parsed_table['parsed', 'from'] =='parse error')])
            parsed_table[('parsed', 'name')] = parsed_table[('Name(Born–Died)', 'Name(Born–Died)')]
            parsed_table[('parsed', 'party')] = parsed_table[('Party', 'Party.1')]
            parsed_table[('parsed', 'government')] = parsed_table[('Government',      'Government')]
            parsed_table = parsed_table[[x for x in parsed_table.columns if x[0] == 'parsed']]
            parsed_table.columns = parsed_table.columns.droplevel(0)
            self.parsed_tables.append(parsed_table)

    def save_tables(self, names):
        for n, table in enumerate(self.parsed_tables):
            pickle.dump(table, open(f'{store_location}\{names[n]}.pickle', 'wb'))
