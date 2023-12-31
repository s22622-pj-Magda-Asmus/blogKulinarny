from flask import Flask, g, request, redirect, url_for, flash, session
from flask import render_template
import sqlite3 
import random
import string
import hashlib
import binascii
from restapi.recipes_api import recipes_api

#ZJl 
app_info = {
    "db_file" : "C:/Users/Madzialenna/Desktop/blogKulinarny/myBlog/data/recipes.db"
}


app= Flask(__name__)
app.register_blueprint(recipes_api)

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
        self.is_valid = False
        

    def hash_password(self):
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'),  100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    def get_random_user_pasword(self):

        password_characters = string.ascii_letters 
        random_password = ''.join(random.choice(password_characters)for i in range(3))
        self.password = random_password

    def login_user(self):

        db = get_db()
        sql_statement = 'select id, email, password, is_active from users where email=?'
        cur = db.execute(sql_statement, [self.user])
        user_record = cur.fetchone()

        if user_record != None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None   
        
    def get_user_info(self):
        db = get_db()
        sql_statement = 'select email, is_active from users where email=?'
        cur = db.execute(sql_statement, [self.user])
        db_user = cur.fetchone()

        if db_user == None:
            self.is_valid = False
            self.email = ''
        elif db_user['is_active']!=1:
            self.is_valid = False
            self.email = db_user['email']
        else:
            self.is_valid = True
            self.email = db_user['email']


    
@app.route('/init_app')
def init_app():

    db = get_db()
    sql_statement = 'select count(*) as cnt from users where is_active;'
    cur = db.execute(sql_statement)
    active_user = cur.fetchone()

    if active_user!=None and active_user['cnt']>0:
        return redirect(url_for('index'))

    user_pass = UserPass()
    user_pass.get_random_user_pasword()
    sql_statement = '''insert into users(email, password, is_active)
                       values(?,?,True);'''
    db.execute(sql_statement, [ 'xxx@xxx.xx', user_pass.hash_password()])

    db.commit()

    flash('password {} has been created'.format(user_pass.password))
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
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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
    
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

    db = get_db()
    sql_command = 'select * from recipes'
    cur = db.execute(sql_command)
    recipes = cur.fetchall()

    return render_template('myRecipes.html',recipes = recipes )
   
@app.route('/deleteProcess/<int:recipe_id>')
def deleteProcess(recipe_id):

    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))
    
    db=get_db()
    sql_statement = 'delete from recipes where int = ?;'
    db.execute(sql_statement, [recipe_id] )    
    db.commit()


    return redirect(url_for('myRecipes'))


@app.route('/updateProcess/<int:recipe_id>', methods=['GET', 'POST'])
def updateProcess(recipe_id):
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html', active_menu='login')
    else:
        user_email = '' if 'user_email' not in request.form else request.form['user_email']
        password = '' if 'password' not in request.form else request.form['password']

        login = UserPass(user_email, password)
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_email
            return redirect(url_for('index'))
        else:
            flash('Nie udało się zalogować. Spróbuj ponownie')
            return render_template('login.html')
        

@app.route('/logout')
def logout():

    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    message = None
    user = {}

    if request.method == 'GET':
        return render_template('register.html', active_menu='users', user=user)
    else:
        user['user_email'] = '' if 'user_email' not in request.form else request.form['user_email']
        user['password'] = '' if 'password' not in request.form else request.form['password']

        cursor = db.execute('SELECT COUNT(*) AS cnt FROM users WHERE email = ?', [user['user_email']])
        record = cursor.fetchone()
        is_user_email_unique = (record['cnt'] == 0)

        if user['user_email'] == '':
            message = 'Pole z mailem jest wymagane'
        elif user['password'] == '':
            message = 'Pole z hasłem jest wymagane'
        elif not is_user_email_unique:
            message = 'Użytkownik z takim mailem ({}) już istnieje'.format(user['user_email'])

        if not message:
            password = UserPass(user['password'])
            password_hash = password.hash_password()

            sql_statement = '''INSERT INTO users (email, password, is_active) VALUES (?, ?, True);'''
            db.execute(sql_statement, [user['user_email'], password_hash])
            db.commit()

            flash('Użytkownik o adresie email {} został utworzony'.format(user['user_email']))
            return redirect(url_for('login'))
        else:
            flash('Błąd: {}'.format(message))
            return render_template('register.html', active_menu='users', user=user)
        
@app.route('/new_password')
def new_password():

    return render_template('new_password.html')

if __name__=='__main__':
    app.run()