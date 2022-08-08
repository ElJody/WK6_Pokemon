from flask import redirect, render_template, request, url_for, flash
import requests
import time 
from app import app, db
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import FindPokemon, LoginForm, RegisterForm
from .models import User, Pokemon
from .forms import PokemonForm, EditProfileForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print('login POST success')
        if form.validate_on_submit():
            email = form.email.data.lower()
            print(email)
            password = form.password.data
            print(password)

            u = User.query.filter_by(email=email).first()
            print('form validated!!'+str(u))
            if u is None or not u.check_hashed_password(password):
                flash("Incorrect Email/password Combo", "warning")
                return render_template('login.html.j2', form=form)
            print('we have u')
            print(User().hash_password(password))
            print('u.check printed')
            flash('Successfully logged in','warning')
            login_user(u)
            return redirect(url_for('index'))

            

    return render_template('login.html.j2', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            first_name = form.first_name.data.lower()
            last_name = form.last_name.data.lower()
            email=form.email.data
            password =form.password.data
            new_user = User(first_name=first_name, last_name=last_name,email=email,password=User().hash_password(password))
            db.session.add(new_user)
            db.session.commit()
        except:
            flash('Something went wrong!')
            return redirect(url_for('register'))
        flash('You are now registered!', "warning")
        return redirect(url_for('login'))
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
                "ability":data['abilities'][0]["ability"]["name"].title(),
                "base experience":data['base_experience'],
                "photo":data['sprites']['other']['home']["front_default"],
                "attack base stat": data['stats'][1]['base_stat'],
                "hp base stat":data['stats'][0]['base_stat'],
                "defense stat":data['stats'][2]["base_stat"]
            }
        return render_template('pokemon.html.j2', pokemon=poke_dict, form=form) 
    return render_template('pokemon.html.j2', form=form)

@app.route('/catch_pokemon', methods=['GET', 'POST'])
@login_required
def catch_pokemon():
    form = PokemonForm()
    if request.method == 'POST':
        # poke_name = form.poke_name.data.lower()
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string)
        
        data = response.json()
        poke_dict={
            "name": data['name'].lower(),
            "ability":data['abilities'][0]["ability"]["name"].lower(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"],
            "user_id": current_user.id
        }
        new_pokemon = Pokemon(**poke_dict)
#        new_pokemon = Pokemon()
        new_pokemon.from_dict(poke_dict)
        new_pokemon.save_poke()

        poke2 = Pokemon.query.filter_by(name=name.lower()).first()
        print(poke2)
        print(current_user)
        print(current_user.pokemon)
        current_user.pokemon = poke2.id
        print(current_user.pokemon)
        current_user.save()
        poke2.save_poke()

        flash(f'You caught {poke2.name.title()}!', 'success')
        
        return render_template('search.html.j2', pokemon=poke_dict)

    else:
        error = 'error'
        return render_template('search.html.j2', poke=error)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if request.method == 'POST' and form.validate_on_submit():
        edited_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
            }
        
        user = User.query.get(current_user.id)
        if user and user.email != current_user.email:
            flash('Email already exists!', 'danger')
            return redirect(url_for('edit_profile'))
        try:
            current_user.from_dict(edited_user_data)
            current_user.save()
            flash('Profile updated!', 'success')
        except:
            flash('Error updating profile!', 'danger')
            return redirect(url_for('edit_profile'))
        return redirect(url_for('index'))
    return render_template('edit_profile.html.j2', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'info')
    return redirect(url_for('index'))


# #                app.login_user(u)
#                 if login_user(u):
#                     print('login success')
#                     return redirect(url_for('index'))
#                 else:
#                     print('login failed')
#                     return redirect(url_for('login'))
#                return redirect(url_for('index'))