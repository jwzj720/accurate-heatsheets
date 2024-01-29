import os
from dotenv import load_dotenv
import psycopg2
import requests
from typing import Dict, List
import logging 

# Load the environment variables from .env file
load_dotenv('/home/wjones/CC/Capstone/tbd2/LACCTiC/.env', override=True)
logging.basicConfig(filename='db_insert.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get the database credentials from environment variables
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

def insert_race(conn, race_info: Dict, url: str, runner_sex: str = None):
    with conn.cursor() as cur:
        insert_query = """
            INSERT INTO Races (meet_id, meet_name, date, tfrrs_url, section, sex)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (meet_id) 
            DO UPDATE SET 
                tfrrs_url = EXCLUDED.tfrrs_url
        """
        data = (race_info['id'], race_info['meet_name'], race_info['date'], url, race_info['section'], runner_sex)
 
        if runner_sex is not None:
            insert_query += ", sex = EXCLUDED.sex"

        cur.execute(insert_query, data)
        conn.commit()




def insert_race_result(conn, race_id: int, runner_id: int, result: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO RaceResults (meet_id, lacctic_id, time, result)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (meet_id, lacctic_id) DO NOTHING;
        """, (race_id, runner_id, result['time'], result.get('place')))
        conn.commit()

def process_page(conn, page_data: Dict):
    for runner_data in page_data['results']:
        
        runner_sex = None  
        if runner_data.get('team'):
            runner_sex = runner_data['team'].get('sex', None)
        for season_rating in runner_data['season_ratings']:
            # Process XC performances
            #for xc_performance in season_rating.get('season_xc_performances', []):
            #    insert_race(conn, xc_performance['race'], runner_sex)
             #   insert_race_result(conn, xc_performance['race']['id'], runner_data['id'], xc_performance)

            # Process track performances
            for track_performance in season_rating.get('season_track_performances', []):
                insert_race(conn, track_performance['race'], track_performance['url'], runner_sex)
                insert_race_result(conn, track_performance['race']['id'], runner_data['id'], track_performance)


def main():
    # Main script to retrieve and process data
    next_page_url = 'https://c03mmwsf5i.execute-api.us-east-2.amazonaws.com/production/api_ranking/runner_page/?page=2000'
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