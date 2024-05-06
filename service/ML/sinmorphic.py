import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_sinhala_morphology(sentence):
    # URL for the site
    url = "http://nlp-tools.uom.lk/sin-morphy/"

    # Create a session to maintain the state (cookies) across requests
    with requests.Session() as session:
        # Send a GET request to retrieve the initial page and get the form data
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        form_data = {input_tag['name']: input_tag.get('value', '') for input_tag in soup.select('form input')}

        # Add the Sinhala sentence to the form data
        form_data['anaText'] = sentence
        form_data['analyseButton'] = 'Parse'

        # Send a POST request with the form data to simulate the form submission
        response = session.post(url, data=form_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response after the form submission
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table in the HTML content
            table = soup.find('table')

            # Extract table data into a list of lists
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
                table_data.append(row_data)

            # Extract word, type, and description from table data
            result = []
            for row in table_data[1:]:
                if len(row) >= 3:  # Ensure row has at least 3 elements
                    word = row[0]
                    word_type = row[1]
                    description = row[2].replace('\n', ' ').strip()
                    result.append({'word': word, 'type': word_type, 'description': description})

            return result
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
