from flask import render_template, request, abort
from document_retrieval import get_search_results, process_results
import pandas as pd
from project import create_app

app = create_app()
SEARCH_TERM = ''

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search/<search_term>", methods=['GET'])
def search(search_term):
    global SEARCH_TERM
    
    results = get_search_results(search_term)
    if results is None:
        abort(404)
    else:
        # Paginate DataFrame and process results
        per_page = 20
        page = int(request.args.get('page', 1))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_df = results.iloc[start_idx:end_idx]
        table = process_results(page_df)
        
        # Check if a new search is being performed in order to reset the selected keywords
        if search_term==SEARCH_TERM:
            new_search = False
        else:
            SEARCH_TERM = search_term
            new_search = True
        return render_template('results.html', table=table, page=page, per_page=per_page, num_rows=len(results), new_search=new_search)