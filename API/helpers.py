# Helper functions for the Flask app
import shortuuid
import os
import sys
import pandas as pd
from db_query import db_query 

# Get the absolute path of the directory containing the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the sys.path list
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Now you can import modules from the 'utils' directory
from pdf_parser.pdf_parsing import extract_dict_from_heat_sheet


#### GENERAL API HELPERS ####

def allowed_file(filename, ALLOWED_EXTENSIONS): 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_uuid():
    return shortuuid.uuid()

def add_uuid_to_filename(filename,uuid):
    base, extension = os.path.splitext(filename)
    return f"{base}-{uuid}{extension}"
    

#### PDF TO CSV HELPERS ####

# Text processing for database queries
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
            personal_best_time = dbq.get_personal_best(split_name[1], split_name[0], distance, athlete['school'])
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
    
def create_csv(filename,meet_info_from_pdf,download_folder):   
    event_list,name_list,school_list,seed_time_list,year_list,pr_list = create_lists_of_meet_info(meet_info_from_pdf)
    output_df = create_meet_df(event_list,name_list,school_list,
                               seed_time_list,year_list,pr_list)
    
    output_file_name = f"{filename.replace('.pdf','')}_results.csv"
    path_to_output_file = os.path.join(download_folder, output_file_name)
    csv_file = output_df.to_csv(path_to_output_file)
    return csv_file, path_to_output_file
