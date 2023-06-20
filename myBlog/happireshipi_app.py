from flask import Flask, g, request, redirect, url_for, flash
from flask import render_template
import sqlite3 
import random
import string
import hashlib
import binascii


app_info = {
    "db_file" : "C:/Users/Madzialenna/Desktop/blogKulinarny/myBlog/data/recipes.db"
}


app= Flask(__name__)
app.config['SECRET_KEY'] = 'xxx!'
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


class UserPass:
    def __init__(self, user='', password=''):
        self.user = user
        self.password=password

    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'),  100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    def get_random_user_pasword(self):

        password_characters = string.ascii_letters #+ string.digits + string.punctuation
        random_password = ''.join(random.choice(password_characters)for i in range(3))
        self.password = random_password
    
@app.route('/init_app')
def init_app():

    # check if there are users defined (at least one active admin required)
    db = get_db()
    sql_statement = 'select count(*) as cnt from users where is_active;'
    cur = db.execute(sql_statement)
    active_user = cur.fetchone()

    if active_user!=None and active_user['cnt']>0:
        return redirect(url_for('index'))
# if not - create/update admin account with a new password and admin privileges, display random username
    user_pass = UserPass()
    user_pass.get_random_user_pasword()
    sql_statement = '''insert into users(email, password, is_active)
                       values(?,?,True);'''
    db.execute(sql_statement, [ 'xxx@xxx.xx', user_pass.hash_password()])
    db.commit()
    flash('password {} has been created'.format(user_pass.password))
    #print('password {} has been created'.format(user_pass.user, user_pass.password)) 
    return redirect(url_for('index'))

    

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__=='__main__':
    app.run()