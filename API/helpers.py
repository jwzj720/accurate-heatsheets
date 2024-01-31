# Helper functions for the Flask app
import pandas as pd
from API.db_query import db_query 

def distance_to_string(distance):
    if distance == "5000":
        return "5k"
    if distance == "10000":
        return "10k"
    
def split_first_and_last_name(name_str:str):
    if "," in name_str:
        return name_str.replace(" ","").split(",")

def create_lists_of_meet_info(meet_info_from_pdf):
    dbq = db_query() # Database query object
    # creates a seriees of lists with relevant info. to be transformed into a df and then csv
    event_list, name_list, school_list, seed_time_list, year_list, pr_list =[],[],[],[],[],[]
    for event in meet_info_from_pdf:
        distance = distance_to_string(event['distance'])
        event_name = f"{event['gender']}'s {distance}"

        for athlete in event['athletes_list']:
            event_list.append(event_name)

            name_list.append(athlete["name"])
            school_list.append(athlete['school'])
            seed_time_list.append(athlete['time'])
            year_list.append(athlete['year'])

            split_name = split_first_and_last_name(athlete['name'])
            # Query database and add to df
            # TODO there could be a problem here with the team name being correct from heat sheet to database
            personal_best_time = dbq.get_personal_best(split_name[1], split_name[0], athlete['school'], distance)
            pr_list.append(personal_best_time)
    
    return event_list,name_list,school_list,seed_time_list,year_list,pr_list

def create_meet_df(event_list, name_list, school_list, 
                   seed_time_list, year_list, pr_list):
    # Create dataframe
    return pd.DataFrame(
        {
            "Event":event_list,
            "Heat Number":None,
            "School":school_list,
            "Year":year_list,
            "Name":name_list,
            "Seed Time":seed_time_list,
            "Event PR":pr_list
        }
    )
    

def create_csv(filename,meet_info_from_pdf):   
    event_list,name_list,school_list,seed_time_list,year_list,pr_list = create_lists_of_meet_info(meet_info_from_pdf)
    output_df = create_meet_df(event_list,name_list,school_list,
                               seed_time_list,year_list,pr_list)
    
    output_file_name = f"{filename.replace('.','')}_results.csv"
    csv_file = output_df.to_csv(output_file_name)
    return csv_file
