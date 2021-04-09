"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger #not used in this exercise
from flask_cors import CORS #to avoid CORS (Cross-Origin Resource Sharing) domain errors 
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite


app = Flask(__name__)    #create new Flask app
app.url_map.strict_slashes = False    #to allow URL with or without final slash "/"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')  #connect to database specified in file: .env
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #if "true", everytime I modify models.py it creates a migration
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


### User endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/user', methods=['GET'])
def get_all_user():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users)) 
    print("GET all_users: ", all_users)
    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)

    if user is None:
        raise APIException('User not found', status_code=404)

    print("GET single user: ", user)
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    user = User(username=request_body["username"], email=request_body["email"], password=request_body["password"])
    db.session.add(user)
    db.session.commit()
    print("User created: ", request_body)
    return jsonify(request_body), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body = request.get_json()
    user = User.query.get(user_id)

    if user is None:
        raise APIException('User not found', status_code=404)
    if "username" in request_body:
        user.username = request_body["username"]
    if "email" in request_body:
        user.email = request_body["email"]
    if "password" in request_body:
        user.password = request_body["password"]
    
    db.session.commit()

    print("User property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()
    response_body = {
         "msg": "User delete successful",
    }
    return jsonify(response_body), 200


### Character endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/character', methods=['GET'])
def get_all_character():
    all_characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters)) 
    return jsonify(all_characters), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)

    return jsonify(character.serialize()), 200

@app.route('/character', methods=['POST'])
def create_character():
    request_body = request.get_json()
    character = Character(name=request_body["name"], birth_year=request_body["birth_year"],  gender=request_body["gender"], height=request_body["height"], mass=request_body["mass"], home_world=request_body["home_world"])
    db.session.add(character)
    db.session.commit()
    print("Character created: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    request_body = request.get_json()
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)
    if "name" in request_body:
        character.name = request_body["name"]
    if "birth_year" in request_body:
        character.birth_year = request_body["birth_year"]
    if "mass" in request_body:
        character.eye_color = request_body["mass"]
    if "gender" in request_body:
        character.gender = request_body["gender"]
    if "home_world" in request_body:
        character.hair_color = request_body["home_world"]
    if "height" in request_body:
        character.height = request_body["height"]
    
    db.session.commit()

    print("Character property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)

    db.session.delete(character)
    db.session.commit()
    response_body = {
         "msg": "Character delete successful",
    }
    return jsonify(response_body), 200


### Planet endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets)) 
    return jsonify(all_planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)

    return jsonify(planet.serialize()), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    planet = Planet(name=request_body["name"], climate=request_body["climate"], orbital_period=request_body["orbita_period"], population=request_body["population"], rotation_period=request_body["rotation_period"], gravity=request_body["gravity"])
    db.session.add(planet)
    db.session.commit()
    print("Planet created: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    request_body = request.get_json()
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
    if "name" in request_body:
        planet.name = request_body["name"]
    if "climate" in request_body:
        planet.climate = request_body["climate"]
    if "gravity" in request_body:
        planet.diameter = request_body["gravity"]
    if "population" in request_body:
        planet.population = request_body["population"]
    if "rotation_period" in request_body:
        planet.rotation_period = request_body["rotation_period"]
    if "orbital_period" in request_body:
        planet.terrain = request_body["orbital_period"]
    
    db.session.commit()

    print("Planet property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)

    db.session.delete(planet)
    db.session.commit()
    response_body = {
         "msg": "Planet delete successful",
    }
    return jsonify(response_body), 200


### Favorite endpoints:
@app.route('/favorite', methods=['GET'])
def get_all_favorite():
    all_favorites = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), all_favorites)) 
    return jsonify(all_favorites), 200


# These two lines should always be at the end of the main.py file.
# Meaning: only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)