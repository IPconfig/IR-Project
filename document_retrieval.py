# This file contains all functions related to the repository.tudelft.nl website.
import requests
import urllib.parse
import pandas as pd
import re

from collections import Counter

from models import Document


url = "https://repository.tudelft.nl/islandora/search/"

def get_search_results(search_term):
    """ Get search results from repository.tudelft.nl, store in a dataframe and return it."""
    def is_quote_ok(s):
        """ Check if the search term is surrounded by quotes. If not, add them. """
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


def count_topic_frequencies(df, column):
    """ Count the number of times a topic appears in a column of a DataFrame"""
    topic_counter = Counter()
    for topics in df[column]:
        if topics:
            topic_list = [topic.strip() for topic in topics.split(';')]
            topic_counter.update(topic_list)
    return topic_counter

def display_frequencies(counter):
    """ Format the topic frequencies for display """
    formatted_frequencies = "; ".join([f"{topic} ({count})" for topic, count in counter.items()])
    return formatted_frequencies

def process_results(csv_data: pd.DataFrame):
    """ Convert DataFrame to list of Document objects """
    results = []
    csv_data = csv_data.fillna('') # convert NaN values to empty strings
    
    topic_frequencies = count_topic_frequencies(csv_data, 'subject topic')
    
    for _, row in csv_data.iterrows(): 
        subject_topics = row['subject topic']
        # add the number of times a topic appears in the results to the topic
        if subject_topics:
            topic_list = [topic.strip() for topic in subject_topics.split(';')]
            updated_topics = "; ".join([f"{topic} ({topic_frequencies[topic]})" for topic in topic_list])
        else:
            updated_topics = ""
            
    # Replace everything between the parenthesis with 'Author' for each author in the list
        if row['author']:
            authors_cleaned = ';'.join([re.sub(r'\(.*?\)', ' (Author)', author).strip() for author in row['author'].split(';')])
        else:
            authors_cleaned = ""
            
        results.append(Document(
            uuid= row['uuid'],
            title= row['title'],
            date = row['publication year'],
            authors= authors_cleaned,
            subjects= updated_topics,
            abstract= row['abstract'],
            doctype= row['publication type'],
            publisher= row['publisher'],
            series = row['faculty'], #TODO: change the series variable to faculty
            collection= row['department'] #TODO: change the collection variable to department    
        ))       

    return results

def filter_documents(documents, keywords):
    """ Filter the documents based on the selected keywords """
    filtered_documents = []

    for document in documents:
        if any(keyword in document.subjects.split(';') for keyword in keywords):
            filtered_documents.append(document)

    return filtered_documents
