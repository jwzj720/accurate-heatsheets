import os
from dotenv import load_dotenv
import psycopg2
from typing import Dict, List
import logging 

load_dotenv('/home/wjones/CC/Capstone/tbd2/Track/.env', override=True)

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
    
    def get_personal_best(self, first_name: str, last_name: str, distance: str, team: str = None) -> None:
        first_name_pattern = f'%{first_name}%'
        last_name_pattern = f'%{last_name}%'
        team_name_pattern = f'%{team}%' if team else None
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
        elif distance == '1500m':
            one = '1500m'
            two = '1500'
            three = '1,500m'
            four = '1,500'
            five = '1500m'
            six = '1500'
        elif distance == '3000m':
            one = '3000m'
            two = '3000'
            three = '3,000m'
            four = '3,000'
            five = '3000m'
            six = '3000'
        elif distance == '800m':
            one = '800m'
            two = '800'
            three = '800m'
            four = '800'
            five = '800m'
            six = '800'
        else:
            return
        with self.conn.cursor() as cur:
            if team:
                cur.execute("""
                    SELECT 
                    rn.firstname,
                    rn.lastname,
                    rn.team_name AS team_name,
                    MIN(rr.time) AS personal_best_time
                    FROM 
                        Runners rn
                    JOIN 
                        RaceResults rr ON rn.tfrrs_id = rr.tfrrs_id
                    JOIN 
                        Races r ON rr.tfrrs_meet_id = r.tfrrs_meet_id
                    WHERE 
                        rn.firstname ILIKE %s AND 
                        rn.lastname ILIKE %s AND
                        rn.team_name ILIKE %s AND
                        (
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s
                        )
                    GROUP BY 
                        rn.firstname, rn.lastname, rn.team_name;
                    """, (
                    first_name_pattern, last_name_pattern, team_name_pattern,
                    f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'))
            else:
                cur.execute("""
                    SELECT 
                    rn.firstname,
                    rn.lastname,
                    MIN(rr.time) AS personal_best_time
                    FROM 
                        Runners rn
                    JOIN 
                        RaceResults rr ON rn.tfrrs_id = rr.tfrrs_id
                    JOIN 
                        Races r ON rr.tfrrs_meet_id = r.tfrrs_meet_id
                    WHERE 
                        rn.firstname ILIKE %s AND 
                        rn.lastname ILIKE %s AND
                        (
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s
                        )
                    GROUP BY 
                        rn.firstname, rn.lastname;
                    """, (
                    first_name_pattern, last_name_pattern,
                    f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'))
            result = cur.fetchone()
            if result and result[3]:
                return(result[3])
            elif result and result[2]: 
                return(result[2])
            else:
                return(None)

    def get_season_best(self, first_name: str, last_name: str, year: int, distance: str,team : str = None) -> None:
        first_name_pattern = f'%{first_name}%'
        last_name_pattern = f'%{last_name}%'
        team_name_pattern = f'%{team}%' if  team else None
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
        elif distance == '1500m':
            one = '1500m'
            two = '1500'
            three = '1,500m'
            four = '1,500'
            five = '1500m'
            six = '1500'
        elif distance == '3000m':
            one = '3000m'
            two = '3000'
            three = '3,000m'
            four = '3,000'
            five = '3000m'
            six = '3000'
        elif distance == '800m':
            one = '800m'
            two = '800'
            three = '800m'
            four = '800'
            five = '800m'
            six = '800'
        else:
            return
        with self.conn.cursor() as cur:
            if team:
                cur.execute("""
                    SELECT 
                    rn.firstname,
                    rn.lastname,
                    rn.team_name AS team_name,
                    MIN(rr.time) AS personal_best_time
                    FROM 
                        Runners rn
                    JOIN 
                        RaceResults rr ON rn.tfrrs_id = rr.tfrrs_id
                    JOIN 
                        Races r ON rr.tfrrs_meet_id = r.tfrrs_meet_id
                    WHERE 
                        rn.firstname ILIKE %s AND 
                        rn.lastname ILIKE %s AND
                        rn.team_name ILIKE %s AND
                        r.date ILIKE %s AND
                        (
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s
                        )
                    GROUP BY 
                        rn.firstname, rn.lastname, rn.team_name;
                    """, (
                    first_name_pattern, last_name_pattern, team_name_pattern, '%' + str(year) + '%',
                    f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'))
            else:
                cur.execute("""
                    SELECT 
                    rn.firstname,
                    rn.lastname,
                    MIN(rr.time) AS personal_best_time
                    FROM 
                        Runners rn
                    JOIN 
                        RaceResults rr ON rn.tfrrs_id = rr.tfrrs_id
                    JOIN 
                        Races r ON rr.tfrrs_meet_id = r.tfrrs_meet_id
                    WHERE 
                        rn.firstname ILIKE %s AND 
                        rn.lastname ILIKE %s AND
                        r.date ILIKE %s AND 
                        (
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s OR
                            r.section ILIKE %s
                        )
                    GROUP BY 
                        rn.firstname, rn.lastname;
                    """, (
                    first_name_pattern, last_name_pattern, '%' + str(year) + '%',
                    f'%{one}%', f'%{two}%', f'%{three}%', f'%{four}%', f'%{five}%', f'%{six}%'))
            result = cur.fetchone()
            if result and result[3]:
                return(result[3])
            elif result and result[2]: 
                return(result[2])
            else:
                return(None)