import json
import requests
from assets.headers import vtheader

# Define the URL for the search request
SEARCH_URL = "https://www.virustotal.com/ui/search"
# Define headers to match the intercepted request
headers = vtheader

file_hash = "000e565854d24a54e6a853d7119dbe598a329b0340aa044f222e1b02c371c599"

def analysis_stats (data) :
    analysis_results = data.get("data", [])[0].get("attributes", {}).get("last_analysis_stats", []).get("malicious")
    return analysis_results


def process_response(response):
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            data = response.json()

            # check if the file is malicious at the first point
            stat = analysis_stats(data)

            # only if malicious number is greater than 0
            if stat > 0: return True
            else: return False
            
        except json.JSONDecodeError:
            print("Response is not valid JSON")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# this somewhat bypasses the api restriction somewhat maybe
def virusTotalWeb(file_hash):

    isMalacious = False
    # Define the parameters for the search query
    params = {
        "limit": 20,
        "relationships[comment]": "author,item",
        "query": file_hash,
    }

    try:
        # Make a GET request to the search URL with headers and parameters
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        isMalacious = process_response(response)

        return isMalacious

    except Exception as e: print(f"An error occurred: {str(e)}")
 