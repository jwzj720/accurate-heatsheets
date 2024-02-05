import requests
import json

api_url = "https://c03mmwsf5i.execute-api.us-east-2.amazonaws.com/production/api_ranking/runner_page/"
url = api_url  # Initial URL without page parameter
lookup_table = {}  # Dictionary to store name-ID pairs

# Loop through pages until there are no more results
while url:
    # Send a get request to the current URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the runners' information from the current page
        results = data.get("results", [])
        for runner in results:
            runner_id = runner.get("id")
            firstname = runner.get("firstname")
            lastname = runner.get("lastname")

            # Combine first name and last name to create a full name
            full_name = f"{firstname} {lastname}"

            # Add the name-ID pair to the lookup table
            lookup_table[full_name] = runner_id

        # Check if there are more pages of results
        next_page = data.get("next")
        if next_page:
            url = next_page  # Set the URL for the next page
        else:
            url = None  # No more pages, exit the loop
    else:
        print(f"Error: {response.status_code}")
        break

# Print the lookup table
for name, runner_id in lookup_table.items():
    print(f"Runner Name: {name}, Runner ID: {runner_id}")

