import os
from dotenv import load_dotenv
import psycopg2
import requests
from typing import Dict, List
import logging 
import csv
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

def get_team_id(conn, team_name):
    with conn.cursor() as cur:
        cur.execute("SELECT team_id FROM teams WHERE name = %s;", (team_name,))
        result = cur.fetchone()
        return result[0] if result else None

def get_lacctic_id(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(lacctic_id), 0) + 1 FROM runners;")
        result = cur.fetchone()
        return result[0] if result else None

def insert_or_update_runner(conn, runner_data):
    with conn.cursor() as cur:
        # Step 1: Check if a runner with the given tffrs_id exists
        cur.execute("SELECT lacctic_id FROM runners WHERE tffrs_id = %s;", (runner_data['tffrs_id'],))
        if cur.fetchone():
            # Runner with this tffrs_id already exists, do nothing
            return

        # Step 2: Check if a runner with the same firstname and lastname exists
        cur.execute("SELECT lacctic_id, team_id FROM runners WHERE firstname = %s AND lastname = %s;", (runner_data['first_name'], runner_data['last_name']))
        results = cur.fetchall()
        if results:
            if len(results) == 1:
                # Only one runner with this firstname and lastname, update tffrs_id
                cur.execute("UPDATE runners SET tffrs_id = %s WHERE lacctic_id = %s;", (runner_data['tffrs_id'], results[0][0]))
            else:
                # Multiple runners with the same firstname and lastname, resolve using team_id
                team_id = get_team_id(conn, runner_data['team_name'])
                for lacctic_id, existing_team_id in results:
                    if existing_team_id == team_id:
                        # Found a matching runner with the same team_id, update tffrs_id
                        cur.execute("UPDATE runners SET tffrs_id = %s WHERE lacctic_id = %s;", (runner_data['tffrs_id'], lacctic_id))
                        break
        else:
            # Step 3: No matching runner found, insert a new runner
            new_lacctic_id = get_lacctic_id(conn)
            cur.execute("""
                INSERT INTO runners (lacctic_id, firstname, lastname, team_id, tffrs_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (new_lacctic_id, runner_data['first_name'], runner_data['last_name'], get_team_id(conn, runner_data['team_name']), runner_data['tffrs_id']))
        conn.commit()

def main():
    conn = connect_db(db_params)
    with open('CSV/new_runners_parsed_with_names_split.csv', 'r') as file:
        reader = csv.DictReader(file)
        runners_from_csv = [row for row in reader]
    for runner in runners_from_csv:  
        #print(runner)
        insert_or_update_runner(conn, runner)
    conn.close()
    logging.info('Runner data inserted into database')

if __name__ == '__main__':
    main()