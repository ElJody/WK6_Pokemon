from app import db
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash



# user_poke = db.Table("user_poke",
#     db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")),
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
# )

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

    def delete(self):
        db.session.delete(self) # remove the user from the session
        db.session.commit() # save the stuff in the session to the database