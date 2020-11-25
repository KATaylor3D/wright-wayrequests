import sqlite3
import os
import Scraper


main_directory = os.getcwd()
temp_directory = main_directory + '\\temp'

n = '\n'

column_values = [
                'Identifying_Number TEXT',
                'Name TEXT',
                'Stage TEXT',
                'Age TEXT',
                'Intake_Date TEXT',
                'Species TEXT',
                'Breed TEXT',
                'Sex TEXT',
                'Size TEXT',
                'Color TEXT',
                'Declawed TEXT',
                'House_Trained TEXT',
                'Location TEXT',
                'Spayed_Neutered TEXT',
                'Description TEXT',
                'Photo_Link_1 TEXT',
                'Photo_Link_2 TEXT',
                'Photo_Link_3 TEXT'
                ]


def search_syntax(tups):
    search_strings = []
    for title, param in tups:
        structured_string = f"{title} LIKE '%{param}%'"
        search_strings.append(structured_string)
    if len(tups) == 1:
        return 'WHERE ' + search_strings[0]
    else:
        search = 'WHERE ' + ' AND '.join(search_strings)
        return search

class Database():

    def __str__(self):
        return "<class 'Sqlick.Database'>"

    def __init__(self, columns = ''):
        self.db = 'Sqlick.db'
        self.table = 'Main'
        self.columns = ', '.join(columns)
        self.data_size = len(columns)
        self.methods = ['get_column_titles',
                        'get_unique_data_of_column',
                        'get_data_equal_to_values_in_columns',
                        'get_data_by_index',
                        'add_data',
                        'delete_data',
                        'refactor_table']
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        if columns:
            c.execute(f"CREATE TABLE IF NOT EXISTS {self.table} ({self.columns})")
        conn.commit()
        conn.close()



    def get_column_titles(self):
        conn = sqlite3.connect(self.db)
        c = conn.execute(f'select * from {self.table}')
        columns_titles = [description[0] for description in c.description]
        conn.close()
        return columns_titles

    def get_unique_data_of_column(self, column_title):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        if isinstance(column_title, str):
            data = [titles[0] for titles in c.execute(f"SELECT {column_title} FROM {self.table}")]
        else:
            data = []
            for title in column_title:
                c.execute(f"SELECT {title} FROM {self.table}")
                data.append(c.fetchall())
        conn.close()
        data = list(set(data))
        return data
    
    def get_data_equal_to_values_in_columns(self, search_params):
        search = search_syntax(search_params)
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {self.table} {search}")
        data = c.fetchall()
        conn.commit()
        conn.close()
        return list(data[0])

    def get_data_by_index(self, index = 0):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {self.table}')
        full_table = c.fetchall()
        conn.close()
        if isinstance(index, tuple) or isinstance(index, list):
            return full_table[index[0]-1 : index[1]]
        elif index == 0:
            return full_table
        elif index > 0:
            return full_table[index-1]

    def add_data(self, data):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        pass_in_length = '(' + (("?," * self.data_size)[:-1]) + ')'
        c.execute(f'INSERT INTO {self.table} VALUES {pass_in_length}', data)
        conn.commit()
        conn.close()

    def delete_data(self, location):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        if (isinstance(location, tuple) or isinstance(location, list)) and len(location) == 2:
            if location[0] < location[1]:
                for segments in range(location[0], location[1] +1):
                    c.execute(f'DELETE from {self.table} WHERE rowid = {segments}')
            else:
                for segments in range(location[1], location[0] +1):
                    c.execute(f'DELETE from {self.table} WHERE rowid = {segments}')
        elif isinstance(location, tuple) or isinstance(location, list):
            for loc in location:
                c.execute(f'DELETE from {self.table} WHERE rowid = {loc}')
        else:
            c.execute(f'DELETE from {self.table} WHERE rowid = {location}')
        conn.commit()
        conn.close()
        self.refactor_table()

    def refactor_table(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(f"CREATE TABLE temp ({self.columns})")
        c.execute(f'INSERT INTO temp SELECT * FROM {self.table}')
        c.execute(f'DROP TABLE {self.table}')
        c.execute(f"CREATE TABLE {self.table} ({self.columns})")
        c.execute(f'INSERT INTO {self.table} SELECT * FROM temp')
        c.execute('DROP TABLE temp')
        conn.commit()
        conn.close()



def create_temp_database():
    os.chdir(temp_directory)
    Scraper.update_data()
    os.chdir(main_directory)

def remove_temp_database():
    os.chdir(temp_directory)
    os.remove("Sqlick.db")
    os.chdir(main_directory)

def get_new_ids():
    os.chdir(temp_directory)
    db = Database(column_values)
    temp_ids = db.get_unique_data_of_column('Identifying_Number')
    os.chdir(main_directory)
    db = Database(column_values)
    main_ids = db.get_unique_data_of_column('Identifying_Number')
    new_ids = list(set(temp_ids) - set(main_ids))
    return new_ids

def get_new_data():
    new_ids = get_new_ids()
    os.chdir(temp_directory)
    db = Database(column_values)
    new_data = []
    for ids in new_ids:
        search_list = [['Identifying_Number', ids]]
        data = db.get_data_equal_to_values_in_columns(search_list)
        new_data.append(data)
    os.chdir(main_directory)
    return new_data

def add_data_to_main_database(data):
    new_data = data
    db = Database(column_values)
    for data in new_data:
        db.add_data(list(data))

def add_singular_data_to_main_database(data):
    db = Database(column_values)
    db.add_data(list(data))

if __name__ == '__main__':
    print("Not run directly")