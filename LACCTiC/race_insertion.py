import os
from dotenv import load_dotenv
import psycopg2
import requests
from typing import Dict, List
import logging 

# Load environment variables from .env file
load_dotenv('/home/wjones/CC/Capstone/tbd2/LACCTiC/.env', override=True)
logging.basicConfig(filename='db_insert.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get database credentials from environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Connect to the database
db_params = {
    'dbname': db_name,
    'user': db_user,
    'password' : db_password,
    'host' : db_host,
    'port' : db_port
}
def connect_db(db_params):
    """Connect to the PostgreSQL database server."""
    conn = psycopg2.connect(**db_params)
    return conn
def insert_race(conn, race: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Races (meet_id, meet_name, section, tfrrs_url, date, sex, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (meet_id) DO NOTHING;
        """, (race['id'], race['meet_name'], race['section'], race['tfrrs_url'], race['date'], race['sex'], race['location']))
        conn.commit()
def insert_race_result(conn, race_id: int, result: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO RaceResults (meet_id, lacctic_id, time, result)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (meet_id, lacctic_id) DO NOTHING;
        """, (race_id, result['runner']['id'], result['time'], result['place']))
        conn.commit()
def process_page(conn, page_data: Dict):
    for race_data in page_data['results']:
        # Insert race data
        insert_race(conn, race_data)
        xc_results = race_data['xc_results'] if race_data.get('xc_results') else []
        track_results = race_data['track_results'] if race_data.get('track_results') else []

        # Insert results
        for xc_result in xc_results:
            insert_race_result(conn, race_data['id'], xc_result)
        for track_result in track_results:
             insert_race_result(conn, race_data['id'], track_result)

def main():
    # Main script to retrieve and process data
    next_page_url = 'https://c03mmwsf5i.execute-api.us-east-2.amazonaws.com/production/api_ranking/race_page/'
    page_count = 0
    max_pages = 100000
    conn = connect_db(db_params)
    while next_page_url and page_count < max_pages:
        response = requests.get(next_page_url)
        if response.status_code == 200:
            data = response.json()
            process_page(conn, data)
            #test(data)
            next_page_url = data.get('next')  # Get the next page URL
            #print(next_page_url)
            page_count += 1
            #logging.info(f'Successfully processed page {page_count}')
        else:
            logging.error(f'Error with page {page_count + 1}: {response.status_code}')
            break
    conn.close()
if __name__ == '__main__':
    main()