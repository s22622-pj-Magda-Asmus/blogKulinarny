from flask import Flask
from flask import render_template


app= Flask(__name__)

# from app import routes

@app.route('/')
@app.route('/index')
def index():

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


if __name__=='_main_':
    app.run()