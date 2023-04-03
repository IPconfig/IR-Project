from flask import render_template

from project import create_app
from models import Document

app = create_app()


@app.route("/")
def index():
    doc = Document(
        title='The Great British Sorting Machine: Adolescents’ future in the balance of family, school and the neighborhood',
        date='2018',
        authors='Mijs, Jonathan J.B. (author), Nieuwenhuis, J.G. (author)',
        abstract='Research calls attention to the divergent school and labor market trajectories of&lt;br/&gt;Europe’s youth while, across the Atlantic, researchers describe the long-lasting&lt;br/&gt;consequences of poverty on adolescent development. In this paper we incorporate both processes to shed a new light on a classic concern in the sociology of stratification: how...',
        doctype='working paper',
        subjects=['Adolescents, neighborhood effects, education, cultural resource perspective, reference group theory, United Kingdom, ALSPAC'],
        publisher='London School of Economics and Political Science',
        series='Working Papers - LSE International Inequalities Institute (26)',
        collection='Institutional Repository'
    )


    return render_template('search.html', documents=[doc, doc, doc])
