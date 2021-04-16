"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger #not used in this exercise
from flask_cors import CORS #to avoid CORS (Cross-Origin Resource Sharing) domain errors 
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite


###########
#importaciones para JWT security token

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

###########


app = Flask(__name__)    #create new Flask app
jwt = JWTManager(app)   #variable for security token
app.config["JWT_SECRET_KEY"] = os.environ.get('TOKEN_KEY')  #fetched from .env embedded in .gitignore for security reasons
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


### User endpoints [GET, POST, PUT, DELETE]: 
@app.route('/user', methods=['GET'])
def get_all_user():
    users= User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data["id"] = user.id #borrar luego para efectos de privacidad backend
        user_data["public_id"] = user.public_id
        user_data["username"] = user.username
        user_data["password"] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)
    
    return jsonify({"users": output}), 200

@app.route('/user/<public_id>', methods=['GET'])
def get_single_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()


    if not user:
        return jsonify({"message": "no user found"}), 404

    user_data= {}
    user_data["public_id"] = user.public_id
    user_data["username"] = user.username
    user_data["password"] = user.password
    user_data["admin"] = user.admin
    user_data["id"]= user.id

    return jsonify({"user": user_data}), 200

@app.route('/user', methods=['POST']) #implementación de public_id para privatizar mi id de primary key
def create_user():
    request_body = request.get_json()

    # hashed_password = generate_password_hash(request_body["password"], method='sha256')
    new_user = User(public_id= str(uuid.uuid4()), username = request_body["username"], password=request_body["password"], email=request_body["email"], admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "new user created"}), 200

@app.route('/user/<public_id>', methods=['PUT'])
def update_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "no user found"}), 404
    # if "username" in request_body:
    #     user.username = request_body["username"]
    # if "email" in request_body:
    #     user.email = request_body["email"]
    # if "password" in request_body:
    #     user.password = request_body["password"]

    user.admin = True
    db.session.commit()

    #print("User property updated: ", request_body)
    return jsonify({"message": "this user is now an admin"}), 200

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "user not found"}), 401

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user was deleted"}), 200


### Character endpoints [GET, POST, PUT, DELETE]: 
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


### Favorite endpoints [GET, POST, PUT, DELETE]:

@app.route('/favorite', methods=['GET'])
@jwt_required()
def handle_favorite():
    favorites = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify({"favorites": all_favorites}), 200

@app.route('/favorite', methods=['POST'])
@jwt_required()
def create_favorite():
    current_user = get_jwt_identity()
    body = request.get_json()
    new_favorite = Favorite(item_id=new_favorite["item_id"], item_type=new_favorite["item_type"], user_id=new_favorite["user_id"])

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"new favorite": body}), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(id):
    current_user = get_jwt_identity()
    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({ "msg" : "Favorite deleted successfully" }), 200


### Create user token for the session
@app.route("/login", methods=["POST"]) 
def login():

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username, password=password).first()

    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)



# These two lines should always be at the end of the main.py file.
# Meaning: only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)