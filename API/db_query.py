import os
from dotenv import load_dotenv
import psycopg2
from typing import Dict, List
import logging 

load_dotenv('/home/wjones/CC/Capstone/tbd2/LACCTiC/.env', override=True)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

class db_query:

    def __init__(self):
        self.db_params = {
            'dbname': db_name,
            'user': db_user,
            'password' : db_password,
            'host' : db_host,
            'port' : db_port
        }
        self.conn = self.connect_db()

          

    def connect_db(self):
        """Connect to the PostgreSQL database server."""
        conn = psycopg2.connect(**self.db_params)
        return conn
    
    def get_personal_best(self, first_name: str, last_name: str, team: str, distance: str) -> None:
        first_name_pattern = f'%{first_name}%'
        last_name_pattern = f'%{last_name}%'
        team_name_pattern = f'%{team}%'
        if distance == '8k':
            one = '8k'
            two = '8,000m'
            three = '8000m'
            four = '8.0k'
            five = "8000"
            six = "8"
        elif distance == '10k':
            one = '10k'
            two = '10,000m'
            three = '10000m'
            four = '10.0k'
            five = "10000"
            six = "10"
        elif distance == '5k':  
            one = '5k'
            two = '5,000m'
            three = '5000m'
            four = '5.0k'
            five = "5000"
            six = "5"
        elif distance == '6k':
            one = '6k'
            two = '6,000m'
            three = '6000m'
            four = '6.0k'
            five = "6000"
            six = "6"
        else:
            print("Invalid distance")
            return
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                rn.firstname,
                rn.lastname,
                t.name AS team_name,
                MIN(rr.time) AS personal_best_time
            FROM 
                Runners rn
            JOIN 
                RaceResults rr ON rn.lacctic_id = rr.lacctic_id
            JOIN 
                Races r ON rr.meet_id = r.meet_id
            JOIN 
                Teams t ON rn.team_id = t.team_id
            WHERE 
                rn.firstname ILIKE %s AND 
                rn.lastname ILIKE %s AND
                t.name ILIKE %s AND
                (
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s
                )
            GROUP BY 
                rn.firstname, rn.lastname, t.name;
            """, (
            first_name_pattern, last_name_pattern, team_name_pattern,
            f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'
        ))
            
            result = cur.fetchone()
            if result:
                return(result[3])
            else:
                return(None)

    def get_season_best(self, first_name: str, last_name: str, team : str, year: int, distance: str) -> None:
        first_name_pattern = f'%{first_name}%'
        last_name_pattern = f'%{last_name}%'
        team_name_pattern = f'%{team}%'
        if distance == '8k':
            one = '8k'
            two = '8,000m'
            three = '8000m'
            four = '8.0k'
            five = "8000"
            six = "8"
        elif distance == '10k':
            one = '10k'
            two = '10,000m'
            three = '10000m'
            four = '10.0k'
            five = "10000"
            six = "10"
        elif distance == '5k':  
            one = '5k'
            two = '5,000m'
            three = '5000m'
            four = '5.0k'
            five = "5000"
            six = "5"
        elif distance == '6k':
            one = '6k'
            two = '6,000m'
            three = '6000m'
            four = '6.0k'
            five = "6000"
            six = "6"
        else:
            print("Invalid distance")
            return
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                rn.firstname,
                rn.lastname,
                t.name AS team_name,
                MIN(rr.time) AS personal_best_time
            FROM 
                Runners rn
            JOIN 
                RaceResults rr ON rn.lacctic_id = rr.lacctic_id
            JOIN 
                Races r ON rr.meet_id = r.meet_id
            JOIN 
                Teams t ON rn.team_id = t.team_id
            WHERE 
                rn.firstname ILIKE %s AND 
                rn.lastname ILIKE %s AND
                t.name ILIKE %s AND
                EXTRACT(YEAR FROM r.date) = %s AND
                (
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s OR
                    r.section ILIKE %s
                )
            GROUP BY 
                rn.firstname, rn.lastname, t.name;
            """, (
            first_name_pattern, last_name_pattern, team_name_pattern, str(year),
            f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'))
            result = cur.fetchone()
            if result:
                return(result[3])
            else:
                return(None)