from flask import Flask, g, request
from flask import render_template
import sqlite3 

app_info = {
    "db_file" : "C:/Users/Madzialenna/Desktop/blogKulinarny/myBlog/data/recipes.db"
}


app= Flask(__name__)

# from app import routes
def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info["db_file"])
        conn.row_factory=sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db    

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    sql_command = 'select * from recipes'
    cur = db.execute(sql_command)
    transactions = cur.fetchall()

    return render_template('index.html',transactions = transactions )

@app.route('/addRecipe')
def addRecipe():

    return render_template('addRecipe.html')


@app.route('/addProcess', methods=['POST'])
def addProcess():

    nazwa = 'emptyString'
    if 'nazwa' in request.form:
        nazwa = request.form['nazwa']

    skladniki = 'emptyString'
    if 'skladniki' in request.form:
        skladniki = request.form['skladniki']

    przygotowanie = 'emptyString'
    if 'przygotowanie' in request.form:
        przygotowanie = request.form['przygotowanie']

    img='logo.png'

    db = get_db()
    sql_command = "insert into recipes(nazwa,skladniki,przygotowanie, img) values (?,?, ?,?)"
    db.execute(sql_command, [nazwa, skladniki, przygotowanie, img])
    db.commit()

    body= f'A wiec nazwa dania to {nazwa} a składniki to {skladniki} a przygotowanie to {przygotowanie}'

    return body

@app.route('/myRecipes', methods=['GET'])
def myRecipes():
    db = get_db()
    sql_command = 'select * from recipes'
    cur = db.execute(sql_command)
    transactions = cur.fetchall()

    return render_template('myRecipes.html',transactions = transactions )
   



if __name__=='__main__':
    app.run()