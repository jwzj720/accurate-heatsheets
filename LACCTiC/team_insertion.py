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
    #print(team)
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO teams (team_id, name, sex)
            VALUES (%s, %s, %s) ON CONFLICT (team_id) DO NOTHING; 
        """, (team['id'], team['name'], team['sex']))
        conn.commit()
def process_page(conn, page: Dict):
    for team in page['results']:
        insert_team(conn, team)
def main():
    # Main script to retrieve and process data
    next_page_url = 'https://c03mmwsf5i.execute-api.us-east-2.amazonaws.com/production/api_ranking/search_teams/'
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