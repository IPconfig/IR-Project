
from flask import render_template, request, abort, redirect
from document_retrieval import get_search_results, process_results, filter_documents
import pandas as pd
import math

from project import create_app
from models import Document

app = create_app()
SEARCH_TERM = ''
DOCUMENT_LIST = []

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
    global DOCUMENT_LIST
    
    per_page = 20
    query = request.args.get("query", type=str, default=None)
    if query is None: abort(403)
    selected_keywords = request.args.get("selected_keywords", type=str, default=None)

    if selected_keywords:
        selected_keywords = selected_keywords.split(',')
    # Check if a new search is being performed in order to reset the selected keywords
    if query==SEARCH_TERM:
        clear_local_storage = False
    else:
        SEARCH_TERM = query
        DOCUMENT_LIST = []
        clear_local_storage = True
    
    if not DOCUMENT_LIST:    
        # search for documents
        results = get_search_results(query)
        if results is None:
            abort(404)
        else:
            DOCUMENT_LIST = process_results(results) # table is a list of documents

    if selected_keywords:
        filtered_documents = filter_documents(DOCUMENT_LIST, selected_keywords)
        print(filtered_documents)
    else:
        filtered_documents = DOCUMENT_LIST
    
    total_documents = len(filtered_documents)
    print(f'total documents: {total_documents}')
    total_pages = math.ceil(total_documents / per_page)
    
    page = int(request.args.get('page', 1))


    return render_template('search.html', documents=filtered_documents, query=query, total_documents=total_documents, page = page, total_pages = total_pages, clear_local_storage=clear_local_storage)


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