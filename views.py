from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "Missing arguments"
        abort(400)

    if session.query(User).filter_by(username=username).first() is None:
        print("Existing User")
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'user already exists'}), 200
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurant_handler():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])

    elif request.method == 'POST':
        # MAKE A NEW RESTAURANT AND STORE IN DB
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        restaurant_info = findARestaurant(mealType, location)
        if restaurant_info:
            restaurant = Restaurant(restaurant_name=unicode(restaurant_info['name'], restaurant_address=unicode(restaurant_info['address'], restaurant_image=unicode(restaurant_info['image'])
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant=restaurant.serialize)
        else:
            return jsonify({"error": "No Restaurants Found for %s in %s" % (mealType, location)})

@app.route('/restaurants/<int:id>', methods=['GET', 'POST', 'DELETE'])
def restaurant_handler(restaurant):
    restaurant=session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'GET':
        # return one restaurant
        return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'POST':
        # UPDATE SPECIFIC RESTAURANT
        address=request.args.get('address')
      	image=request.args.get('image')
      	name=request.args.get('name')
        if address:
      		restaurant.restaurant_address=address
      	if image:
      		restaurant.restaurant_image=image
      	if name:
      		restaurant.restaurant_name=name
      	session.commit()
      	return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'DELETE':
        # DELETE A SPECFIC RESTAURANT
        session.delete(restaurant)
        session.commit()
        return "Restaurant Deleted"

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)
