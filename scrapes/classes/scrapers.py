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

def parse_us_date(rawdate):
    rawmon, rawday, rawyear = rawdate.split(' ')
    for n, m in enumerate(months_choice):
        if m == rawmon:
            mon = n + 1
    day = int(rawday.replace(',', ''))

    return dt.date(int(rawyear[:4]), mon, day)

def split_from_to_dates(x, f_or_t):
    try:
        from_date, to_date = x.split('–')
        if f_or_t == 'f':
            return parse_us_date(from_date)
        else:
            return parse_us_date(to_date)
    except:
        return 'parsing error'


class WikiScraper():
    def __init__(self, url):
        self.url = url
        self.raw_tables = []
        self.parsed_tables = []
        self.parse_errors = []

    def scrape_tables(self, tables_to_keep=None):
        tables = pd.read_html(self.url)
        if tables_to_keep is not None:
            tables = [tables[i] for i in tables_to_keep]
        self.raw_tables = tables

    def parse_tables_uk(self):
        for raw_table in self.raw_tables:
            parsed_table = raw_table.copy()
            parsed_table['from'
            ] = parsed_table[parsed_table.columns[3]].apply(from_to_date_parser)
            parsed_table['to'
            ] = parsed_table[parsed_table.columns[4]].apply(from_to_date_parser)
            parsed_table['name'] = parsed_table[parsed_table.columns[2]]
            parsed_table['party'] = parsed_table[parsed_table.columns[7]]
            parsed_table['government'] = parsed_table[parsed_table.columns[8]]
            parsed_table['Monarch'] = parsed_table[parsed_table.columns[9]]
            parsed_table = parsed_table[['from', 'to', 'name', 'party', 'government']]
            parsed_table.columns = parsed_table.columns.get_level_values(0)
            parsed_table.drop_duplicates(inplace=True)

            self.parse_errors.append(parsed_table[(parsed_table['to'] == 'parsing error') | (parsed_table['from'] == 'parsing error')])
            parsed_table = parsed_table[
                (parsed_table['to'] != 'parsing error') & (parsed_table['from'] != 'parsing error')]
            parsed_table['country'] = 'UK'
            parsed_table['type'] = 'gov'
            self.parsed_tables.append(parsed_table)

    def parse_tables_us(self):
        for raw_table in self.raw_tables:
            parsed_table = raw_table.copy()
            parsed_table['name'] = parsed_table[('President')]
            parsed_table['government'] = parsed_table['name']
            parsed_table['party'] = parsed_table['Party[b].1']
            parsed_table['from'] = parsed_table['Presidency[a].1'].apply(split_from_to_dates, f_or_t='f')
            parsed_table['to'] = parsed_table['Presidency[a].1'].apply(split_from_to_dates, f_or_t='t')

            self.parse_errors.append(parsed_table[(parsed_table['to'] =='parsing error') | (parsed_table['from'] =='parsing error')])
            parsed_table = parsed_table[(parsed_table['to'] !='parsing error') & (parsed_table['from'] !='parsing error')]
            parsed_table = parsed_table[['name', 'government', 'party', 'from', 'to']]
            parsed_table.drop_duplicates(inplace=True)
            parsed_table['country'] = 'US'
            parsed_table['type'] = 'gov'
            self.parsed_tables.append(parsed_table)

    def parse_tables_gr(self):
        """ too difficult """
        for raw_table in self.raw_tables:
            parsed_table = raw_table.copy()
            parsed_table[('parsed', 'from')
            ] = parsed_table[('Term of office',     'Took office')].apply(from_to_date_parser)
            parsed_table[('parsed', 'to')
            ] = parsed_table[('Term of office', 'Left office')].apply(from_to_date_parser)
            self.parse_errors.append(parsed_table[(parsed_table[('parsed', 'to')] == 'parsing error') | (parsed_table[('parsed', 'from')] == 'parsing error')])
            parsed_table = parsed_table[
                (parsed_table[('parsed', 'to')] != 'parsing error') & (parsed_table[('parsed', 'from')] != 'parsing error')]
            parsed_table[('parsed', 'name')] = parsed_table[('Name(Born–Died)', 'Name(Born–Died)')]
            parsed_table[('parsed', 'party')] = parsed_table[('Party', 'Party.1')]
            parsed_table[('parsed', 'government')] = parsed_table[('Government',      'Government')]
            parsed_table = parsed_table[[x for x in parsed_table.columns if x[0] == 'parsed']]
            parsed_table.columns = parsed_table.columns.droplevel(0)
            self.parsed_tables.append(parsed_table)

    def parse_tables_it(self):
        for raw_table in self.raw_tables:
            parsed_table = raw_table.copy()
            parsed_table[('parsed', 'from')
            ] = parsed_table[('Term of office',     'Took office')].apply(from_to_date_parser)
            parsed_table[('parsed', 'to')
            ] = parsed_table[('Term of office', 'Left office')].apply(from_to_date_parser)
            self.parse_errors.append(parsed_table[(parsed_table[('parsed', 'to')] == 'parsing error') | (parsed_table[('parsed', 'from')] == 'parsing error')])
            parsed_table = parsed_table[
                (parsed_table[('parsed', 'to')] != 'parsing error') & (parsed_table[('parsed', 'from')] != 'parsing error')]
            parsed_table[('parsed', 'name')] = parsed_table[('Name(Born–Died)', 'Name(Born–Died)')]
            parsed_table[('parsed', 'party')] = parsed_table[('Party', 'Party.1')]
            parsed_table[('parsed', 'government')] = parsed_table[('Government',      'Government')]
            parsed_table = parsed_table[[x for x in parsed_table.columns if x[0] == 'parsed']]
            parsed_table.columns = parsed_table.columns.droplevel(0)
            parsed_table['country'] = 'Italy'
            parsed_table['type'] = 'gov'
            self.parsed_tables.append(parsed_table)

    def save_tables(self, output_name):
        final_table = pd.concat(self.parsed_tables, axis=0)
        pickle.dump(final_table, open(f'{store_location}\{output_name}.pickle', 'wb'))
