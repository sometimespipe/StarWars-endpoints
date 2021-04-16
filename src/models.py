from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# For each 'model` I have to declare a class with the model properties 
# and a method `serialize` that returns a dictionary representation of the class

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, default=True)
    admin = db.Column(db.Boolean(), default=False)
    favorites = db.relationship('Favorite', backref='User') # One to Many

    # __repr__():  tell python how to print the class object in the console
    def __repr__(self):
        return '<User: %r>' % self.username

    # serialize(): tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "public_id": self.user_id,
            # do not serialize the password, its a security breach
        }
    

class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=False, nullable=False) # store character_id or planet_id
    item_type = db.Column(db.String(80), unique=False, nullable=False) # type can be Character or Planet
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_id": self.item_id, 
            "item_type": self.item_type
        }


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    mass = db.Column(db.Float, unique=False, nullable=False)
    home_world = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Character: %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "home_world": self.home_world, 
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Float, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String(50), unique=False, nullable=False)
    rotation_period = db.Column(db.Float, unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet: %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "rotation_period": self.rotation_period
        }
    