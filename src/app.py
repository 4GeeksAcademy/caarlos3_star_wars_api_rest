"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import select
from models import db, User, Planets, Characters, FavoritesPlanet, FavoritesCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_get_users():

    all_users = db.session.execute(select(User)).scalars().all()
    all_users = list(map(lambda user: user.serialize(), all_users))
    response_body = {
        "users": all_users
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def handle_create_users():
    body = request.get_json()

    if 'email' not in body or 'password' not in body:
        return jsonify( {"err": "Datos requeridos no incluidos"}), 400
    
    user = User()
    user.email = body['email']
    user.password = body['password']

    db.session.add(user)
    db.session.commit()


    return jsonify({"ok": True}), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():

    all_planets = db.session.execute(select(Planets)).scalars().all()
    all_planets = list(map(lambda planets: planets.serialize(), all_planets))
    response_body = {
        "users": all_planets
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_get_planet_from_id(planet_id):
    planet = db.session.get(Planets, planet_id)
    if planet is None:
        return jsonify({"err": "Planet not found"}), 404
    
    response_body={
        "planet": planet.serialize()
    }
    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def handle_get_characters():

    all_characters = db.session.execute(select(Characters)).scalars().all()
    all_characters = list(map(lambda characters: characters.serialize(), all_characters))
    response_body = {
        "users": all_characters
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_get_character_from_id(character_id):
    character = db.session.get(Characters, character_id)
    if character is None:
        return jsonify({"err": "Planet not found"}), 404
    
    response_body={
        "charcater": character.serialize()
    }
    return jsonify(response_body), 200


@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_favorites_from_user_id(user_id):
    get_favlist_for_planets = select(FavoritesPlanet).where(FavoritesPlanet.user_id == user_id)
    favorites_planets = db.session.execute(get_favlist_for_planets).scalars().all()

    get_favlist_for_character = select(FavoritesCharacter).where(FavoritesCharacter.user_id == user_id)
    favorites_character = db.session.execute(get_favlist_for_character).scalars().all()

    planets_favorite_list = [favorites.serialize() for favorites in favorites_planets]
    characters_favorite_list = [favorites.serialize() for favorites in favorites_character]

    response = {
        "favorite_planets": planets_favorite_list,
        "favorite_character": characters_favorite_list
    }

    return jsonify(response), 200


@app.route('/favorites/planet/<int:user_id>', methods=['POST'])
def add_favorite_planet(user_id):
    body = request.get_json()
    planet_id = body.get('planet_id')

    if not planet_id:
        return jsonify(
            {'err': 'Planet not found'}, 400
        )
    
    is_favorited = select(FavoritesPlanet).where(
        (FavoritesPlanet.user_id == user_id) & (FavoritesPlanet.planet_from_id == planet_id)
    )

    its_exist= db.session.execute(is_favorited).scalars().first()

    if its_exist:
        return jsonify({'msg': 'Ya añadido en favoritos'}), 400


    favorite = FavoritesPlanet(user_id=user_id, planet_from_id = planet_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado a favoritos"}), 201


@app.route('/favorites/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    search_in_list = select(FavoritesPlanet).where(
        (FavoritesPlanet.user_id == user_id) & (FavoritesPlanet.planet_from_id == planet_id)
    )

    its_exist_in_list = db.session.execute(search_in_list).scalars().first()

    if not its_exist_in_list:
        return jsonify({'err': 'Favorite not search'}), 404
    
    db.session.delete(its_exist_in_list)
    db.session.commit()

    return jsonify({'ok': 'Favorite eliminated'}), 200


@app.route('/favorites/character/<int:user_id>', methods=['POST'])
def add_favorite_character(user_id):
    body = request.get_json()
    character_id = body.get('character_id')

    if not character_id:
        return jsonify(
            {'err': 'Character not found'}, 400
        )
    
    is_favorited = select(FavoritesCharacter).where(
        (FavoritesCharacter.user_id == user_id) & (FavoritesCharacter.character_from_id == character_id)
    )

    its_exist= db.session.execute(is_favorited).scalars().first()

    if its_exist:
        return jsonify({'msg': 'Ya añadido en favoritos'}), 400


    favorite = FavoritesCharacter(user_id=user_id, character_from_id = character_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Character agregado a favoritos"}), 201




@app.route('/favorites/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_character_favorite(user_id, character_id):
    search_in_list = select(FavoritesCharacter).where(
        (FavoritesCharacter.user_id == user_id) & (FavoritesCharacter.character_from_id == character_id)
    )

    its_exist_in_list = db.session.execute(search_in_list).scalars().first()

    if not its_exist_in_list:
        return jsonify({'err': 'Favorite not search'}), 404
    
    db.session.delete(its_exist_in_list)
    db.session.commit()

    return jsonify({'ok': 'Favorite eliminated'}), 200   





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
