from flask import render_template, request
import requests
from app import app 
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import FindPokemon, LoginForm, RegisterForm
from .models import User

# *** I'm thinking this block of code is necessary somwhere ***
# app = Flask(__name__)
# app.config.from_object(Config)
# db= SQLAlchemy(app)
# migrate=Migrate(app,db)
# basic_auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth()

@app.route('/', methods=['GET'])
def index():
    form=FindPokemon()
    return render_template('index.html.j2', form=form)

@app.route('/login', methods=['GET'])
def login():
    form=LoginForm()
    return render_template('login.html.j2', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    return render_template('register.html.j2', form=form)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = FindPokemon()
    if request.method =='POST':
        pokemon_name = form.pokemon_name.data
        print(pokemon_name)
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
                "base experience":data['base_experience'],
                "photo":data['sprites']['other']['home']["front_default"],
                "attack base stat": data['stats'][1]['base_stat'],
                "hp base stat":data['stats'][0]['base_stat'],
                "defense stat":data['stats'][2]["base_stat"]
            }
        return render_template('pokemon.html.j2', pokemon=poke_dict, form=form) 
    return render_template('pokemon.html.j2', form=form)
