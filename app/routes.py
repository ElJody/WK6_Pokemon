from flask import render_template, request
import requests
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        
        data = response.json()

        poke_dict={
            "name": data.json()['name'].title(),
        }
        return render_template('index.html.j2', pokes=poke_dict)
    else:
        error = 'error'
        return render_template('index.html.j2', poke=error)
