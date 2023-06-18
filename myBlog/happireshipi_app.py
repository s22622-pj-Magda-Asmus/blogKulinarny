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

    # if request.method== 'GET' :
    #     return render_template('index.html', title='Home',  posts=posts)
    # else:
    #     if nazwa in request.form:
    #         nazwa = request.form['nazwa']
    #     if skladniki in request.form:
    #         skladniki = request.skladniki['skladniki']
    #     if przygotowanie in request.form:
    #         przygotowanie = request.form['przygotowanie']


    # nazwa= request.form[]    
    # db = get_db()
    # sql_command="insert into recipes(nazwa,skladniki,przygotowanie, img) values (?,?, ?, 'logo.png')"
    # db.execute(sql_command, [nazwa, skladniki, przygotowanie])
    # db.commit

    posts = [
        {
        "id" : 1,
        "nazwa" : "Spaghetti Bolognese",
        "skladniki": "400g spaghetti, 500g mielonej wołowiny, 1 cebula, posiekana, 2 ząbki czosnku, posiekane, 1 puszka pomidorów w kostkach, 2 łyżki koncentratu pomidorowego, 1 łyżeczka suszonego oregano, Sól i pieprz do smaku, Starty ser Parmesan do dekoracji",
        "przygotowanie": "1. Gotuj spaghetti zgodnie z instrukcjami na opakowaniu.\n2. Na dużym garnku, podsmaż mieloną wołowinę z posiekaną cebulą i czosnkiem.\n3. Dodaj pomidory w kostkach, koncentrat pomidorowy, suszone oregano, sól i pieprz. Gotuj na wolnym ogniu przez 20 minut.\n4. Podawaj sos na ugotowanym spaghetti. Posyp startym serem Parmesan.",
        "img": 'logo.png'
        },
        {
        "id" : 2,
        "nazwa": "Kurczak w stir-fry",
        "skladniki": "2 filety z kurczaka, pokrojone w plastry, 1 czerwona papryka, pokrojona w plastry, 1 żółta papryka, pokrojona w plastry, 1 mała cebula, pokrojona w plastry, 2 ząbki czosnku, posiekane, 2 łyżki sosu sojowego, 1 łyżka sosu ostrygowego, 1 łyżka mąki kukurydzianej, 2 łyżki oleju roślinnego, Sól i pieprz do smaku",
        "przygotowanie": "1. W małej misce wymieszaj sos sojowy, sos ostrygowy i mąkę kukurydzianą.\n2. Rozgrzej olej roślinny w woku lub dużej patelni na wysokim ogniu.\n3. Dodaj plastry kurczaka i smaż, aż się zarumieni. Wyjmij z woka.\n4. Do tego samego woka dodaj pokrojone papryki, cebulę i posiekany czosnek. Smaż przez 3-4 minuty.\n5. Wróć kurczaka do woka i wlej przygotowaną mieszankę sosową. Smaż jeszcze przez 2-3 minuty.\n6. Dopraw solą i pieprzem. Podawaj gorące z gotowanym ryżem.",
        "img": 'logo.png'
        },
        {
        "id" : 3,
        "nazwa": "Sałatka Caprese",
        "skladniki": "2 duże dojrzałe pomidory, 8 oz świeżego sera mozzarella, Świeże liście bazylii, Oliwa z oliwek extra virgin, Glazura balsamiczna, Sól i pieprz do smaku",
        "przygotowanie": "1. Na półmisku ułóż plastry pomidorów i sera mozzarella, naprzemiennie.\n2. Wsyp między plastry świeże liście bazylii.\n3. Polej oliwą z oliwek i glazurą balsamiczną.\n4. Dopraw solą i pieprzem. Podawaj od razu.",
        "img": 'logo.png'
        },
        {
        "id" : 4,
        "nazwa": "Ciasteczka czekoladowe",
        "skladniki": "1 szklanka masła, miękkiego, 1 szklanka cukru, 1 szklanka brązowego cukru, 2 duże jajka, 1 łyżeczka ekstraktu z wanilii, 3 szklanki mąki pszennej, 1 łyżeczka sody oczyszczonej, 1/2 łyżeczki soli, 2 szklanki kawałków czekolady",
        "przygotowanie": "1. Rozgrzej piekarnik do 190°C. Przygotuj blachy do pieczenia wyłożone papierem do pieczenia.\n2. W dużej misce ucieraj miękkie masło z cukrem i brązowym cukrem, aż powstanie jednolita masa.\n3. Dodaj jajka i ekstrakt waniliowy. Kontynuuj ucieranie.\n4. W osobnej misce wymieszaj mąkę, sodę oczyszczoną i sól.\n5. Stopniowo dodawaj suchą mieszankę do miski z masłem i cukrem, mieszając do połączenia.\n6. Dodaj kawałki czekolady i wymieszaj, aby były równomiernie rozłożone w cieście.\n7. Formuj małe kulki z ciasta i układaj na przygotowanych blachach, zachowując odstępy.\n8. Piecz przez około 10-12 minut, aż brzegi ciasteczek będą złote. Wyjmij z piekarnika i pozostaw do ostygnięcia na blachach przez kilka minut, a następnie przenieś na kratkę do całkowitego ostygnięcia.",
        "img": 'logo.png'
        }
    ]

    return render_template('index.html', title='Home',  posts=posts)

@app.route('/addNew')
def addNew():

#     body = '''
#         <div style="margin: 25px; background-color:rgb(237, 232, 130); ">
#         <h2 style="margin-top: 100px; padding: 20px;">Dodaj nowe danie do bloga:</h2>
#         <form id="addNew_form" action="/addProcess" method="POST" style="padding: 20px;">
#             <div class="form-group">
#                 <label for="nazwa">Nazwa dania</label>
#                 <input class="form-control" type="text" name="nazwa" id="nazwa" aria-describedby="nazwaInput" placeholder="Wpisz nazwe dania"
#                     maxlength="30">
#             </div>
#             <div class="form-group">
#                 <label for="skladniki">Składniki</label>
#                 <textarea  class="form-control" type="text" id="skladniki" name="skladniki" placeholder="Składniki" maxlength="500"></textarea >
#             </div>
#             <div class="form-group">
#                 <label for="przygotowanie">Przygotowanie</label>
#                 <textarea class="form-control" id="przygotowanie" type="text" name="przygotowanie" placeholder="Opis wykonania" maxlength="500"></textarea>
#             </div>
#             <button type="submit" value="Send" class="btn btn-primary" >Dodaj</button>
#         </form>
#         </div>
#     '''
#     return render_template('addRecipe.html', title='dodawanie przepisu')
#     # return body
    return render_template('addRecipe.html', title='Home')


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



if __name__=='__main__':
    app.run()