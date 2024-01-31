import re

# Use regex to replace multiple consecutive spaces with a single space
def remove_redudant_spaces(input_string):
    cleaned_string = re.sub(r'[ ]+', ' ', input_string)
    return cleaned_string
# Recursivley remove all trailing spaces at the end of stringd
def remove_trailing_space(input_string):
    if input_string[-1] == " ":
        return remove_trailing_space(input_string[:-1])
    else: 
        return input_string
# Use regex to find a number followed by a letter and add a newline
# This is a common PDF error
def add_newline_after_number(input_string):
    pattern = re.compile(r'(\d)([A-Za-z])')
    result = pattern.sub(r'\1\n\2', input_string)
    return result

# Use regex to fix another common PDF error
def add_newline_before_keyword(keywords_list, text):
    for keyword in keywords_list:
        pattern = re.compile(rf'(?<=.)({re.escape(keyword)})', re.IGNORECASE)
        modified_text = pattern.sub(r'\n\1', text)
        text = modified_text
    return modified_text