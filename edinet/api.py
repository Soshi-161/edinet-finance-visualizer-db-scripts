import os
import requests

import my_class as my_class
import lib as lib

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
        # print('preview first data: \n', data[0])  # Print the first document for preview

        # Preview of documents with type code 120 (Annual securities reports) that are not fund reports
        cnt = 0  # Initialize the counter outside the loop
        for doc in data:
            if doc.doc_type_code == '120' and not doc.fund_code:
                print(f"\n Content: {doc} \n")
                cnt += 1
            if cnt >= 10:
                print("Showing preview of first 10 matching documents only.")
                break
                

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
# fetch_list_documents('2024-06-21')

def fetch_document(
        doc_id: str,
):
    """
    Fetch a specific document from the EDINET API.

    Args:
        doc_id (str): The document ID to fetch.

    Returns:
        dict: The document data.
    """

    url = f'{BASE_URL}/documents/{doc_id}'
    params = {
        'Subscription-Key': os.getenv('EDINET_API_KEY'),
        'type': '1',
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        data = response
        print(f"Fetched document with ID {doc_id}.")

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def test():
    data = fetch_document('S100TMQ7')
    unzipped_data = lib.unzip_edinet_xbrl(data.content)
    # print(f"Unzipped data: {unzipped_data.keys()}")  # Print the keys of the unzipped data

    # Search for files with keys starting with '0105'
    target_files = {}
    for k, v in unzipped_data.items():
        filename = os.path.basename(k)  # Extract the filename from the path
        if filename.startswith('0105'):
            target_files[k] = v

    keys= []

    # Print the number of matching files and their names
    if target_files:
        print(f"Found {len(target_files)} matching files:")
        for key in target_files.keys():
            print(f"- {key}")
            keys.append(key)
    else:
        print("No files with keys starting with '0105' found.")
    for _ in range(len(keys)):
        print(f"Parsing file: {keys[_]}")
        
        # Parse the XBRL content and print the result
        print(lib.parse_xbrl(unzipped_data[keys[_]]), "\n\n")

test()