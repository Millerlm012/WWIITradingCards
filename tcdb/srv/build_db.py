"""
TCDB: Tradiong Card Database
- https://www.tcdb.com/ViewSet.cfm/sid/254515/1977-Edito-Service-World-War-II
"""

import os
import requests
import sqlite3
from bs4 import BeautifulSoup


DB_PATH = '/data/trading.db'
PHOTOS_PATH = ''


def init_db():
    """
    Init's the db if it doesn't exist
    """
    if not os.path.isfile(DB_PATH):
        print('Creating trading.db...')

        con = sqlite3.connect(DB_PATH)
        with open('/data/db_schema.sql') as schema:
            con.executescript(schema.read())
        con.commit()
        con.close()

        print('Created trading.db!')

def check_db(table, con):
    cur = con.cursor()
    count = cur.execute(f'SELECT COUNT(*) FROM {table};').fetchone()[0]
    return count

def compile_deck_urls(http, con):
    if check_db('decks', con) == 108:
        print('Decks table already compiled!')
        return

    print('Compiling decks table...')
    soup = BeautifulSoup(http, 'html.parser')
    cur = con.cursor()
    for link in soup.find_all('a'):
        if 'Edito-Service World War II -' in link.text:
            full_name = link.text
            s = link.text.split(' - ')
            publisher = s[0]
            deck_name = s[1]
            deck_number = None
            if 'Deck' in deck_name:
                deck_number = s[1].split(' ')[1]
            cur.execute("INSERT INTO decks (full_name, publisher, deck_name, deck_number, url) VALUES (?, ?, ?, ?, ?)",
                        (full_name, publisher, deck_name, deck_number, f'https://tcdb.com/{link.get("href")}'))
    con.commit()
    print('Compiled decks table!')

def compile_card_urls(http, con):
    cur = con.cursor()

def compile_urls(con):
    print('--- Compiling urls... ---')
    req = requests.get('https://www.tcdb.com/ViewSet.cfm/sid/254515/1977-Edito-Service-World-War-II')
    compile_deck_urls(req.text, con)
    compile_card_urls(req.text, con)
    print('--- Compilation complete! ---')

def fetch_images(con):
    cur = con.cursor()
    data = cur.execute("SELECT id, full_name, publisher, deck_name, deck_number, url FROM decks").fetchall()
    cards = [
        {'id': card[0],
         'full_name': card[1],
         'publisher': card[2],
         'deck_name': card[3],
         'deck_number': card[4],
         'url': card[5]
         }
        for card in data]
    print(cards)
    # TODO: complete logic for compiling data for each trading card


def build_db():
    con = sqlite3.connect(DB_PATH)
    compile_urls(con)
    fetch_images(con)


if __name__ == '__main__':
    print('--- Database init ---')
    init_db()
    print('--- Database init complete ---')

    print('--- Build database ---')
    build_db()
    print('--- Database built ---')