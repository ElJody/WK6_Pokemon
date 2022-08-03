from flask import render_template, request
import requests
from app import app
from app.forms import FindPokemon

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = FindPokemon()
    if request.method =='POST':
        pokemon_name = form.pokemon_name.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "No Pokemon Found, Try Again..."
            return render_template('pokemon.html.j2', error=error_string,form=form)
        data = response.json()
        for pokemon in data:
            poke_dict={}
            poke_dict={
                "name": data['name'].title(),
                "ability":data['abilities'][0]["ability"]["name"],
                "base experiance":data['base_experience'],
                "photo":data['sprites']['other']['home']["front_default"],
                "attack base stat": data['stats'][1]['base_stat'],
                "hp base stat":data['stats'][0]['base_stat'],
                "defense stat":data['stats'][2]["base_stat"]
            }
        return render_template('pokemon.html.j2', pokemon=poke_dict, form=form) 
    return render_template('pokemon.html.j2', form=form)
