"""
TCDB: Tradiong Card Database
- https://www.tcdb.com/ViewSet.cfm/sid/254515/1977-Edito-Service-World-War-II
"""

import os
import requests
import shutil
import sqlite3
from bs4 import BeautifulSoup


DB_PATH = '/data/trading.db'
IMAGES_PATH = '/data/images'


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

def check_table_and_create(table, con):
    print(f'Checking table {table}...')

    cur = con.cursor()
    table_count = len(cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';").fetchall())

    if table_count == 0:
        print(f'{table} doesn\'t exist... Creating it now')
        with open('/data/db_schema.sql') as f:
            table_schemas = f.read()

        table_schemas.split('--') # the first element is blank, all preceeding elements are schemas in order
        if table == 'decks':
            cur.execute(table_schemas[1])
        elif table == 'cards':
            cur.execute(table_schemas[2])

        con.commit()
        print(f'{table} created!')
    else:
        print(f'{table} exists!')


    print(f'Table check for {table} complete!')
    return table_count

def process_card_id(id):
    return id.replace('#', '').replace('-', '_').replace(' ', '_')

def compile_deck_urls(http, con):
    if check_db('decks', con) == 108:
        print('Decks table already compiled!')
        return

    print('Compiling decks table...')
    soup = BeautifulSoup(http, 'html.parser')
    cur = con.cursor()
    for link in soup.find_all('a'):
        if 'Edito-Service World War II -' in link.text:
            if 'Deck 125' in link.text:
                continue

            full_name = link.text
            s = link.text.split(' - ')
            publisher = s[0]
            deck_name = s[1]
            deck_number = None
            if 'Deck' in deck_name:
                deck_number = s[1].split(' ')[1]
            cur.execute("INSERT INTO decks (full_name, publisher, deck_name, deck_number, url) VALUES (?, ?, ?, ?, ?)",
                        (full_name, publisher, deck_name, deck_number, f'https://www.tcdb.com{link.get("href")}'))
    con.commit()
    print('Compiled decks table!')

def download_image(url, download_path):
    print(f'Downloading image {url}...')

    req = requests.get(url, stream=True)
    assert req.status_code == 200, f'Ope, something went wrong downloading an image from {url}.'

    with open(download_path, 'wb') as f:
        f.raw.decode_content = True
        shutil.copyfileobj(req.raw, f)

    print(f'Downloaded image completed successfully!')

def compile_card_urls_and_images(http, con):
    print('Compiling cards table...')

    cur = con.cursor()
    data = cur.execute("SELECT id, full_name, publisher, deck_name, deck_number, url FROM decks").fetchall()
    decks = [
        {'id': deck[0],
         'full_name': deck[1],
         'publisher': deck[2],
         'deck_name': deck[3],
         'deck_number': deck[4],
         'url': deck[5]
         }
        for deck in data]

    for deck in decks:
        print(f'Compiling cards for deck "{deck["deck_name"]}"...')

        deck_req = requests.get(deck['url'])
        deck_soup = BeautifulSoup(deck_req.text, 'html.parser')
        card_links = []
        for link in deck_soup.find_all('a'):
            href = link.get('href')
            if href:
                if '/ViewCard.cfm/' in href:
                    card_links.append(f'https://www.tcdb.com{href}')
        card_links = list(set(card_links))

        for link in card_links:
            card = {}
            card_req = requests.get(link)
            card_soup = BeautifulSoup(card_req.text, 'html.parser')

            card_id = card_soup.find('h4')
            if card_id.find('a'):
                card['card_id'] = process_card_id(card_id.text.split(' - ')[0])
                card['card_name'] = card_id.find('a').text
            else:
                header_split = card_id.text.split(' - ')
                card['card_id'] = process_card_id(header_split[0])
                card['card_name'] = header_split[1]

            card['url'] = link

            image_urls = []
            for link in card_soup.find_all('a'):
                href = link.get('href')
                if href:
                    if '/Images/Large' in href:
                        image_urls.append(f'https://www.tcdb.com{href}')

            assert len(image_urls) == 2, 'Yo, there\'s more than 2 image_urls... wtf.'
            card['front_image_url'] = image_urls[0]
            card['back_image_url'] = image_urls[1]

            # assuming all images .jpg???
            download_image(card['front_image_url'], f'/data/images/{card["card_id"]}_front.jpg')
            download_image(card['back_image_url'], f'/data/images/{card["card_id"]}_back.jpg')
            cur.execute("INSERT INTO cards (card_id, card_name, url, front_image_url, back_image_url, deck_id) VALUES (?, ?, ?, ?, ?, ?)",
                        (card['card_id'], card['card_name'], card['url'], card['front_image_url'], card['back_image_url'], deck['id']))

        print(f'Completed compilation for {deck["deck_name"]}!')

    con.commit()
    print('Completed compiling ALL decks!')

def compile_urls(con):
    print('--- Compiling urls... ---')
    req = requests.get('https://www.tcdb.com/ViewSet.cfm/sid/254515/1977-Edito-Service-World-War-II')

    check_table_and_create('decks', con)
    compile_deck_urls(req.text, con)

    check_table_and_create('cards', con)
    compile_card_urls_and_images(req.text, con)

    print('--- Compilation complete! ---')


def build_db():
    con = sqlite3.connect(DB_PATH)
    compile_urls(con)


if __name__ == '__main__':
    print('--- Database init ---')
    init_db()
    print('--- Database init complete ---')

    print('--- Build database ---')
    build_db()
    print('--- Database built ---')