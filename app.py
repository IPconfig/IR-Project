
from flask import render_template, request, abort, redirect
from document_retrieval import get_search_results, process_results
import pandas as pd

from project import create_app
from models import Document

app = create_app()
SEARCH_TERM = ''

doc = Document(
    document_id=0,
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
    return render_template('search.html', documents=mock_documents)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get("search-query", type=str, default=None)

    # search for documents

    return render_template('search.html', documents=mock_documents, query=query)


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


@app.route('/sort')
def sort():
    documents = request.args.getlist('documents')
    query =  request.args.get('query',type=str, default=None)
    sort_type = request.args.get('sort_type', type=str, default=None)

    # Sort documents


    return render_template('search.html', documents=mock_documents, query=query)

@app.route("/document")
def document():
    document_id = request.args.get('document_id', type=str, default=None)
    query =  request.args.get('query', type=str, default=None)
    if document_id:

        # Logic for getting specific document

        return render_template('document.html', document=doc, query=query)
    else:
        return redirect('search.html', code=302)