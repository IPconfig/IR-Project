# This file contains all functions related to the repository.tudelft.nl website.
import requests
import urllib.parse
import pandas as pd


url = "https://repository.tudelft.nl/islandora/search/"

def get_search_results(search_term):
    def is_quote_ok(s):
        stack = []
        for c in s:
            if c in ["'", '"', "`"]:
                if stack and stack[-1] == c:
                    # this single-quote is close character
                    stack.pop()
                else:
                    # a new quote started
                    stack.append(c)
            else:
                # ignore it
                pass
        if len(stack) > 0:
            # print(f"s not good {s}")
            for c in stack:
                s += c
            # print(f"new s {s}")
        return s
    
    search_term = is_quote_ok(search_term)
    search_term_encoded = urllib.parse.quote(search_term)
    search_collection = ["", "?collection=research", "?collection=education", "?collection=heritage"]

    save_csv = ["?display=tud_csv", "&display=tud_csv"]

    # search in all collections for now
    search_url = url + search_term_encoded + search_collection[0] + save_csv[0]
    
    response = requests.get(search_url)
    # Check if the response was successful
    if response.status_code == 200:
        # Open the response content as a string buffer
        csv_buffer = response.content.decode('utf-8')
        if "No search results, nothing to export!" in csv_buffer:
            # Handle the case where the CSV file does not exist or is empty
            print('no results found for this search term')
            # results_dict[search_term] = 'no results found'
        else:
            # Read url as a pandas dataframe
            print(search_url)
            try:
                csv_data = pd.read_csv(search_url)
                return csv_data
                # results_dict[search_term] = csv_data
            except pd.errors.ParserError:
                print("something went wrong")
    else:
        print('Failed to download CSV file')


def process_results(csv_data: pd.DataFrame):
    """ Convert DataFrame to list of dictionaries """
    results = []
    csv_data = csv_data.fillna('') # convert NaN values to empty strings
    
    
    for _, row in csv_data.iterrows():        
        subject_topics = row['subject topic'].split("; ")[:9]
        results.append({
            'uuid': row['uuid'],
            'repository_link': row['repository link'],
            'title': row['title'],
            'author': row['author'],
            'contributor': row['contributor'],
            'publication_year': row['publication year'],
            'abstract': row['abstract'],
            'subject_topic': subject_topics
        }) 
    return results