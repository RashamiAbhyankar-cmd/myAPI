from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # Enable CORS for React
DB_NAME = "recipes.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize Database
def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS categories (
    idCategory INTEGER PRIMARY KEY AUTOINCREMENT,
    strCategory TEXT NOT NULL UNIQUE,
    strCategoryThumb TEXT,
    strCategoryDescription TEXT)
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
    idMeal TEXT PRIMARY KEY,
    strMeal TEXT NOT NULL,
    strMealAlternate TEXT,
    strCategory TEXT, -- Foreign key reference
    strArea TEXT,
    strInstructions TEXT,
    strMealThumb TEXT,
    strTags TEXT,
    strYoutube TEXT,
    strIngredient1 TEXT, strIngredient2 TEXT, strIngredient3 TEXT, strIngredient4 TEXT, strIngredient5 TEXT,
    strIngredient6 TEXT, strIngredient7 TEXT, strIngredient8 TEXT, strIngredient9 TEXT, strIngredient10 TEXT,
    strIngredient11 TEXT, strIngredient12 TEXT, strIngredient13 TEXT, strIngredient14 TEXT, strIngredient15 TEXT,
    strIngredient16 TEXT, strIngredient17 TEXT, strIngredient18 TEXT, strIngredient19 TEXT, strIngredient20 TEXT,
    strMeasure1 TEXT, strMeasure2 TEXT, strMeasure3 TEXT, strMeasure4 TEXT, strMeasure5 TEXT,
    strMeasure6 TEXT, strMeasure7 TEXT, strMeasure8 TEXT, strMeasure9 TEXT, strMeasure10 TEXT,
    strMeasure11 TEXT, strMeasure12 TEXT, strMeasure13 TEXT, strMeasure14 TEXT, strMeasure15 TEXT,
    strMeasure16 TEXT, strMeasure17 TEXT, strMeasure18 TEXT, strMeasure19 TEXT, strMeasure20 TEXT,
    strSource TEXT,
    strImageSource TEXT,
    strCreativeCommonsConfirmed TEXT,
    dateModified TEXT,
    FOREIGN KEY (strCategory) REFERENCES categories(strCategory)
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return jsonify([dict(r) for r in recipes])

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q', '')
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes WHERE strCategory LIKE ?', (f'%{query}%',)).fetchall()
    tables=conn.execute('SELECT name FROM sqlite_schema WHERE type="table" AND name NOT LIKE "sqlite_%" ORDER BY name').fetchall()
    conn.close()
    return jsonify({
        "recipes": [dict(r) for r in recipes]
        #"tables": [dict(t) for t in tables]
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    tables=conn.execute('SELECT name FROM sqlite_schema WHERE type="table" AND name NOT LIKE "sqlite_%" ORDER BY name').fetchall()
    
    #categories = conn.execute('SELECT DISTINCT strCategory FROM recipes').fetchall()
    
    conn.close()
    return jsonify({
        "categories": [dict(c) for c in categories],
       # "tables": [dict(t) for t in tables]
    })
    
@app.route('/api/recipes/searchbyMeal', methods=['GET'])
def search_recipesbyMeal():
        query = request.args.get('q1', '')
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes WHERE strMeal LIKE ?', (f'%{query}%',)).fetchall()
        tables=conn.execute('SELECT name FROM sqlite_schema WHERE type="table" AND name NOT LIKE "sqlite_%" ORDER BY name').fetchall()
          
        conn.close()
        return jsonify({
            "recipes": [dict(r) for r in recipes],
            #"tables": [dict(t) for t in tables]
        })
        
@app.route('/api/recipes/searchbyid', methods=['GET'])
def search_recipesbyid():
        query = request.args.get('q2', '')
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes WHERE idMeal LIKE ?', (f'%{query}%',)).fetchall()
        tables=conn.execute('SELECT name FROM sqlite_schema WHERE type="table" AND name NOT LIKE "sqlite_%" ORDER BY name').fetchall()
          
        conn.close()
        return jsonify({
            "recipes": [dict(r) for r in recipes],
            #"tables": [dict(t) for t in tables]
        })

if __name__ == '__main__':
    app.run()
    

