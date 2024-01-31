from PyPDF2 import PdfReader 
from pdf_parser.text_cleaning_tools import *
import os
import re
import json

def extract_text_from_pdf(file):
    reader = PdfReader(file) 
    raw_text = ''
    for page in reader.pages:
        raw_text += page.extract_text() # Add all the pages to one string
    return raw_text

def extract_events_from_text(text):
    # Define regex to find each event in the format (Event)(Number)(Gender)(Distance)(Meters)(Type)
    event_pattern = re.compile(r"(Event).*?(\d+)[^\n]*\n{0,2}?(Women|Men).*?(\d+)[^\n]*\n{0,2}?(Meter)[^\n]*\n{0,2}?(Steeplechase|Run)")

    # find the start and end index of each event within the string
    # will use this to divide the pdf text up into different sections by event
    split_points = []
    iter = event_pattern.finditer(text)
    for match in iter:
        split_points.append((match.start(),match.end()))

    # add events to dictionary
    #TODO there should probably be a "runners" field of each event
    events = []
    event_matches = event_pattern.findall(text)
    for match in event_matches:
        events.append({
            "event_number": match[1],
            "gender":match[2],
            "distance":match[3],
            "type":match[5],
            "athletes_list": []
            })
    return events,split_points

# This function splits the text at different ranges
# The ranges correspond to the location of events within the text
def split_text_at_ranges(input_string, split_ranges):
    result = []
    start_index = 0

    for split_range in split_ranges:
        if isinstance(split_range, tuple) and len(split_range) == 2:
            split_start, split_end = split_range

            if 0 <= split_start < split_end <= len(input_string):
                # Add the part before the range
                result.append(input_string[start_index:split_start])

                # Move the start index to the end of the range
                start_index = split_end

    # Append the remaining part of the string
    result.append(input_string[start_index:])

    return result

# get time. seed, then year, then name, then school,
def find_athlete_in_line(line):
    # patterns for identifying athlete info 
    name_pattern = re.compile(r"([A-Za-z]+, [A-Za-z]+)")
    school_pattern = re.compile(r"((?:[A-Za-z]-?[ ]?)+)")
    year_pattern = re.compile(r"FR|SO|JR|SR|Gr")
    time_pattern = r'\b(?:\d{1,2}:)?\d{1,2}\.\d{1,2}\b'
    seed_pattern = re.compile(r"\d+")
    if line == '':
        return None
    match_count = 0
    modified_text = line

    time = re.findall(time_pattern,modified_text)
    modified_text = re.sub(time_pattern,"",modified_text) # remove pattern from text after finding it

    seed = re.findall(seed_pattern,modified_text) # There should only be one seed time anyway
    modified_text = re.sub(seed_pattern,"",modified_text)

    year = re.findall(year_pattern,modified_text)
    modified_text = re.sub(year_pattern,"",modified_text)

    name = re.findall(name_pattern,modified_text)
    modified_text = re.sub(name_pattern,"",modified_text)

    school = re.findall(school_pattern,modified_text)
    modified_text = re.sub(school_pattern,"",modified_text)
    
    school = None if "Stadium" in school else school # this filters out stadium records
    
    if time: match_count+=1 
    if seed: match_count+=1
    if year: match_count+=1
    if name: match_count+=1
    if school: match_count+=1 
    if match_count < 4:
        return None
    return({
        "name":name[0] if name else None,
        "year":year[0] if year else None,
        "school":remove_trailing_space(school[0]) if school else None,
        "time":time[0] if time else None,
        "seed":seed[0] if seed else None
    })

# Updates events to include runners
def extract_runners_from_text(events,split_string):
    event_count = 0
    for section in split_string[1:]:
        athletes_list = []
        current_event = events[event_count] # find the event the runners are in
        for line in section.split("\n"):
            athlete_dict = find_athlete_in_line(line)
            athletes_list.append(athlete_dict) if athlete_dict else None
        # update the event with the list of athletes
        current_event["athletes_list"] = athletes_list
        event_count+=1
    return events

def extract_dict_from_heat_sheet(heat_sheet_pdf_filename):
    # Extract text 
    raw_text = extract_text_from_pdf(heat_sheet_pdf_filename)
    # cleaning functions
    cleaned_text = remove_redudant_spaces(raw_text)
    cleaned_text = add_newline_after_number(cleaned_text)
    cleaned_text = add_newline_before_keyword(["Event","Yr"], cleaned_text) # Fix instances of [word]Event or [word]Yr
    # Extract events and event location in the text from text
    events,split_points = extract_events_from_text(cleaned_text)
    # Split the full text by events
    split_string = split_text_at_ranges(cleaned_text,split_points)
    # extract runners from text and add to events
    events_with_runners = extract_runners_from_text(events,split_string)

    return(events_with_runners)


