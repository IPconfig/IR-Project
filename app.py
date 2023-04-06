
from flask import render_template, request, abort, redirect
from document_retrieval import get_search_results, process_results
import pandas as pd
import math

from project import create_app
from models import Document

app = create_app()
SEARCH_TERM = ''

doc = Document(
    uuid=0,
    title='The Great British Sorting Machine: Adolescents’ future in the balance of family, school and the neighborhood',
    date='2018',
    authors='Mijs, Jonathan J.B. (author), Nieuwenhuis, J.G. (author)',
    abstract=' In this paper we incorporate both processes to shed a new light on a classic concern in the sociology of stratification: how are adolescents’ aspirations, expectations, and school performance shaped by the combined socioeconomic contexts of family, school and neighborhood life?',
    doctype='working paper',
    subjects='Adolescents; neighborhood effects; education; cultural resource perspective; reference group theory; United Kingdom; ALSPAC',
    publisher='London School of Economics and Political Science',
    series='Working Papers - LSE International Inequalities Institute (26)',
    collection='Institutional Repository'
)

mock_documents = [doc, doc, doc]

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    global SEARCH_TERM
    per_page = 20
    query = request.args.get("query", type=str, default=None)
    if query is None: abort(403)
    # Check if a new search is being performed in order to reset the selected keywords
    if query==SEARCH_TERM:
        clear_selected_topics = False
    else:
        SEARCH_TERM = query
        clear_selected_topics = True
        
    # search for documents
    results = get_search_results(query)
    if results is None:
        abort(404)
    else:
        document_list = process_results(results) # table is a list of documents
        total_documents = len(document_list)
        total_pages = math.ceil(total_documents / per_page)
        
        print(f"total documents: {total_documents}")
        print(f'total pages: {total_pages}')
    
        page = int(request.args.get('page', 1))
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_documents)
        document_slice = document_list[start_idx:end_idx]

    return render_template('search.html', documents=document_slice, query=query, total_documents=total_documents, start_idx=start_idx, end_idx=end_idx, page=page, total_pages = total_pages, new_search=clear_selected_topics)


@app.route('/sort')
def sort():
    documents = request.args.getlist('documents')
    query =  request.args.get('query',type=str, default=None)
    sort_type = request.args.get('sort_type', type=str, default=None)

    # Sort documents


    return render_template('search.html', documents=mock_documents, query=query)

@app.route("/document")
def document():
    document_id = request.args.get('uuid', type=str, default=None)
    query =  request.args.get('query', type=str, default=None)
    if document_id:
        # TODO: get document from list of documents instead of searching again
        
        # search for document_id
        results = get_search_results(document_id)
        if results is None:
            abort(404)
        else:
            doc = process_results(results)[0] # return the first document

        return render_template('document.html', document=doc, query=query)
    else:
        return redirect('search.html', code=302)