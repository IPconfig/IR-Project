from flask import render_template, request, redirect

from project import create_app
from models import Document

app = create_app()

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