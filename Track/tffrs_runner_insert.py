import os
from dotenv import load_dotenv
import psycopg2
import requests
from typing import Dict, List
import logging 
import csv
# Load the environment variables from .env file
load_dotenv('.env', override=True)
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

def insert_or_update_runner(conn, runner_data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO runners (tfrrs_id, firstname, lastname, team_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (runner_data['tffrs_id'], runner_data['first_name'], runner_data['last_name'], runner_data['team_name']))
        conn.commit()

def main():
    conn = connect_db(db_params)
    with open('csv/runners_parsed_with_names_split.csv', 'r') as file:
        reader = csv.DictReader(file)
        runners_from_csv = [row for row in reader]
    for runner in runners_from_csv:  
        insert_or_update_runner(conn, runner)
    conn.close()
    logging.info('Runner data inserted into database')

if __name__ == '__main__':
    main()