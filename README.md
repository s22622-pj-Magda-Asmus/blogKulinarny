# blogKulinarny
Blog about cooking implemented in Flask

To run aplication on Windows:
-open code in IDE and in terminal(bash console)  activate myvenv by running activate script "activate" example command:  ".\myvenv\Scripts\activate"
-from console(with active venv) run command "flask run" and use localhost visible in terminal 

<b>Recipes REST API:</b>
___
Content-Type: application/json\
Accept: application/json
___

* Get all recipes\
GET /recipes


* Get recipe by id\
GET /recipes/search/id/{id}


* Get recipe by name keyword\
GET /recipe/search/id/{id}


* Get recipe with ingredient keyword\
GET /recipe/search/ingredient/{ingredient}


* Add new recipe\
POST /recipe/add

Request body:

{
    "nazwa": "mock",\
    "skladniki": "mock",\
    "przygotowanie": "mock",\
    "img": "mock"
}
