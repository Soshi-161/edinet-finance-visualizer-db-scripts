import os
import requests

import my_class as my_class

EDINET_VERSION = 'v2'
BASE_URL = f'https://api.edinet-fsa.go.jp/api/{EDINET_VERSION}'


def fetch_list_documents(
        date: str,
):
    """
    Fetch the list of documents from the EDINET API.

    Args:
        date (str): The date for which to fetch the documents in YYYY-MM-DD format.

    Returns:
        list: A list of documents.
    """

    url = f'{BASE_URL}/documents.json'
    params = {
        'date': date,
        'type': '2',
        'Subscription-Key': os.getenv('EDINET_API_KEY'),
    }
    try: 
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        data: list[my_class.EdinetDocument] = response.json().get('results', [])
        print(f"Fetched {len(data)} documents for date {date}.")
        data = [my_class.EdinetDocument(**doc) for doc in data]  # Convert to EdinetDocument instances
        print('preview first data: \n', data[0])  # Print the first document for preview

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
# fetch_list_documents('2024-06-21')
