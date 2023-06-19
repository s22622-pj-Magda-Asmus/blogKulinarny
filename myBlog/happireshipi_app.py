from flask import Flask, g, request, redirect, url_for, flash
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
    recipes = cur.fetchall()

    return render_template('index.html',recipes = recipes )

@app.route('/addRecipe')
def addNewRecipe():

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

    return redirect(url_for('myRecipes'))

@app.route('/myRecipes', methods=['GET'])
def myRecipes():
    db = get_db()
    sql_command = 'select * from recipes'
    cur = db.execute(sql_command)
    recipes = cur.fetchall()

    return render_template('myRecipes.html',recipes = recipes )
   
@app.route('/deleteProcess/<int:recipe_id>')
def deleteProcess(recipe_id):
    db=get_db()
    sql_statement = 'delete from recipes where int = ?;'
    db.execute(sql_statement, [recipe_id] )    
    db.commit()


    return redirect(url_for('myRecipes'))


@app.route('/updateProcess/<int:recipe_id>', methods=['GET', 'POST'])
def updateProcess(recipe_id):

    if request.method== 'GET':
        db=get_db()
        sql_statement = "select * from recipes where int = ?;"
        cur = db.execute(sql_statement, [recipe_id])
        recipe = cur.fetchone()

        if recipe==None:
            flash('Nie ma takiego dania')
            return redirect(url_for('myRecipes'))
        else:
            return render_template('editRecipe.html', recipe=recipe)
    else:    
        nazwa = 'emptyString'
        if 'nazwa' in request.form:
            nazwa = request.form['nazwa']

        skladniki = 'emptyString'
        if 'skladniki' in request.form:
            skladniki = request.form['skladniki']

        przygotowanie = 'emptyString'
        if 'przygotowanie' in request.form:
            przygotowanie = request.form['przygotowanie']

        db=get_db()
        sql_command = "update recipes set nazwa=?, skladniki=?, przygotowanie=? where int=?"
        db.execute(sql_command, [nazwa, skladniki, przygotowanie, recipe_id])
        db.commit()


        return redirect(url_for('myRecipes'))



if __name__=='__main__':
    app.run()