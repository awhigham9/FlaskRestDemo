''' Basic Script to initialize the SQLite3 db
    with the correct data
'''
import sqlite3
import csv
import os

CSV_PATH = 'disney_movies.csv'
DB_PATH = 'movies.sqlite3'

def main():
    if os.path.exists(DB_PATH):
        print("Removing existing db. . .")
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    conn.execute('''
        CREATE TABLE movies
        (
            title TEXT PRIMARY KEY ON CONFLICT IGNORE,
            release_date TEXT,
            genre TEXT,
            mpaa_rating TEXT,
            total_gross INTEGER,
            inflation_adjusted_gross INTEGER
        )
    ''')

    with open(CSV_PATH, 'r') as f:
        print('Loading csv. . .')
        reader = csv.reader(f)
        next(reader, None) # Skip the header
        print('Inserting data into db. . .')
        conn.executemany('INSERT INTO movies values (?,?,?,?,?,?)', reader)
        print('Committing transaction. . .')
        conn.commit()


if __name__ == '__main__':
    main()