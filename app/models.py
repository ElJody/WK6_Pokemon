from app import app, db, login

from flask_login import UserMixin
from flask_login import login_user, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

# @app.verify_password
# def verify_password(email, password):
#     u = User.query.filter_by(email=email).first()
#     if u is None:
#         return False
#     current_user = u
#     return u.check_hashed_password(password)

user_poke = db.Table("user_poke",
     db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")),
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
       
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'
    
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self) # add the userr to the session
        db.session.commit() # save the stuff in the session to the database

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    def catch_pokemon(self, poke_dict):
        self.name = poke_dict['name']
        self.ability = poke_dict['ability']
        self.base_experience = poke_dict['base_experience']
        self.attack_base_stat = poke_dict['attack_base_stat']
        self.hp_base_stat = poke_dict['hp_base_stat']
        self.defense_stat = poke_dict['defense_stat']

    def delete(self):
        db.session.delete(self) # remove the user from the session
        db.session.commit() # save the stuff in the session to the database

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    base_experience = db.Column(db.String)
    attack_base_stat = db.Column(db.String)
    hp_base_stat = db.Column(db.String)
    defense_stat = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Pokemon: {self.name}> | Id: {self.id}'

    def from_dict(self, poke_dict):
        self.name = poke_dict['name']
        self.ability = poke_dict['ability']
        self.base_experience = poke_dict['base_experience']
        self.attack_base_stat = poke_dict['attack_base_stat']
        self.hp_base_stat = poke_dict['hp_base_stat']
        self.defense_stat = poke_dict['defense_stat']  

    def save_poke(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()