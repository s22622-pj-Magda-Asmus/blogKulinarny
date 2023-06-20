from flask import jsonify, Blueprint, g, request
from model.recipe import Recipe, RecipeSchema
import sqlite3

recipes_api = Blueprint('recipes_api', __name__)


#################

app_info = {
    "db_file": "C:/Users/Madzialenna/Desktop/blogKulinarny/myBlog/data/recipes.db"
}


def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info["db_file"])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db


@recipes_api.teardown_app_request
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#################


select_all_recipes_sql = 'select * from recipes'
get_recipe_by_id_sql = 'select * from recipes where int = ?;'
add_recipe_sql = 'insert into recipes (nazwa, skladniki, przygotowanie, img) values (?, ?, ?, ?)'


@recipes_api.route('/recipes')
def get_recipes():
    raw_recipes = execute_db_command(select_all_recipes_sql)

    schema = RecipeSchema(many=True)
    recipes = schema.dump(
        raw_recipes
    )

    return jsonify(recipes)


@recipes_api.route('/recipes/search/id/<recipe_id>')
def get_recipe_by_id(recipe_id):
    raw_recipe = execute_db_command(get_recipe_by_id_sql, recipe_id)

    schema = RecipeSchema(many=True)
    recipe = schema.dump(
        raw_recipe
    )

    return jsonify(recipe)


@recipes_api.route('/recipes/search/nameKeyword/<keyword>')
def get_recipes_by_keyword(keyword):
    raw_recipes = execute_db_command(select_all_recipes_sql)
    recipes_objects = map_db_rows_to_recipes(raw_recipes)

    recipes_objects_with_keyword = filter(lambda x: keyword in x.nazwa, recipes_objects)

    schema = RecipeSchema(many=True)
    recipes_with_keyword = schema.dump(
        recipes_objects_with_keyword
    )

    return jsonify(recipes_with_keyword)


@recipes_api.route('/recipes/search/ingredient/<ingredient>')
def get_recipes_with_ingredient(ingredient):
    recipes = execute_db_command(select_all_recipes_sql)
    recipes_objects = map_db_rows_to_recipes(recipes)

    raw_recipes_with_ingredient = filter(lambda x: ingredient in x.skladniki, recipes_objects)

    schema = RecipeSchema(many=True)
    recipes_with_ingredient = schema.dump(
        raw_recipes_with_ingredient
    )

    return jsonify(recipes_with_ingredient)


@recipes_api.route('/recipes/add', methods=['POST'])
def add_recipe():
    title = request.json['nazwa']
    ingredients = request.json['skladniki']
    preparation = request.json['przygotowanie']
    image = request.json['img']

    result = add_db_command(add_recipe_sql, [title, ingredients, preparation, image])

    return jsonify(result)


def execute_db_command(sql_command, param={}):
    db = get_db()
    cur = db.execute(sql_command, param)
    result = cur.fetchall()

    return result


def add_db_command(sql_command, param={}):
    db = get_db()
    db.execute(sql_command, param)
    result = db.commit()

    return result


def map_db_rows_to_recipes(recipes):
    recipe_objects = list()
    for row in recipes:
        recipe: Recipe = Recipe(*row)
        recipe_objects.append(recipe)

    return recipe_objects
