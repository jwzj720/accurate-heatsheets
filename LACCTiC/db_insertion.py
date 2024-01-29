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

def insert_team(conn, team: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Teams (team_id, name, sex, color, logo)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (team['id'], team['name'], team['sex'], team['color'], team['logo']))
        conn.commit()

def insert_runner(conn, runner: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO runners (lacctic_id, tfrrs_id, year_in_school, firstname, lastname, team_id, ability, ability_std, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id; 
        """, (runner['id'], runner['tfrrs_id'], runner['year_in_school'], runner['firstname'], runner['lastname'], runner['team']['id'], runner['ability'], runner['ability_std'], runner['status']))
        inserted_id = cur.fetchone()[0]  
        conn.commit()
        return inserted_id  

def insert_race(conn, race: Dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Races (race_id, meet_name, section, importance, date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (race['id'], race['meet_name'], race['section'], race['importance'], race['date']))
        conn.commit()

def insert_season_rating(conn, season_rating: Dict, id: int):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO "season_ratings" (season_year, runner_id, race_weight_sig, significant, sig_tic, sig_var)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (season_rating['season']['year'], id, season_rating['race_weight_sig'], season_rating['significant'], season_rating['sig_tic'], season_rating['sig_var']))
        season_rating_id = cur.fetchone()[0]
        conn.commit()
    return season_rating_id

def insert_season_xc_performance(conn, performance: Dict, season_rating_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO season_xc_performances (season_rating_id, time, modern_tic, race_weight_sig, significant, race_id, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (season_rating_id, performance['time'], performance['modern_tic'], performance['race_weight_sig'], performance['significant'], performance['race']['id'], performance['race']['date']))
        conn.commit()

def insert_season_track_performance(conn, performance: Dict, season_rating_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Season_track_performances (season_rating_id, time, modern_tic, race_weight_sig, significant, race_id, date, url, meet_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (season_rating_id, performance['time'], performance['modern_tic'], performance['race_weight_sig'], performance['significant'], performance['race']['id'], performance['race']['date'], performance['url'], performance['meet_name']))
        conn.commit()
def update_runner_season_rating(conn, id, season_rating_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Runner
            SET season_rating_id = %s
            WHERE runner_id = %s;
        """, (season_rating_id, id))
        conn.commit()
def process_page(conn, page: Dict):
    for runner in page['results']:
        insert_team(conn, runner['team'])
        id = insert_runner(conn, runner)
        for season_rating in runner.get('season_ratings', []):
            season_rating_id = insert_season_rating(conn, season_rating, id)
            for xc_performance in season_rating.get('season_xc_performances', []):
                insert_race(conn, xc_performance['race'])
                insert_season_xc_performance(conn, xc_performance, season_rating_id)
            for track_performance in season_rating.get('season_track_performances', []):
                insert_race(conn, track_performance['race'])
                insert_season_track_performance(conn, track_performance, season_rating_id)

def main():
    # Main script to retrieve and process data
    next_page_url = 'https://c03mmwsf5i.execute-api.us-east-2.amazonaws.com/production/api_ranking/runner_page/'
    page_count = 0
    max_pages = 100
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
if __name__ == "__main__":
    main()