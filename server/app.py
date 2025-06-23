#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response("<h1>Code challenge</h1>")
    
api.add_resource(Home, "/")

class Restaurants(Resource):
    def get(self):
        restaurants=[restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response(restaurants, 200)
        # restaurants = []
        # restaurant = Restaurant.query.all()
        # for restaurant in restaurants.to_dict():
        #     restaurants.append(restaurant)
        #     return make_response(restaurants, 200)
        
api.add_resource(Restaurants, '/restaurants')     
           
class RestaurantById(Resource):
    def get(self, id):
        restaurant= Restaurant.query.get(id)
        return make_response(restaurant.to_dict(), 200)

    def delete(self, id):
        try:
            restaurant = Restaurant.query.get(id)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response("Restaurant deleted successfully") 
        except Exception as e:
            print(f"{e}")
            return make_response({"error":"Restaurant not found"}, 404)

api.add_resource(RestaurantById, '/restaurants/<int:id>')    

class Pizzas(Resource):
    def get(self):
        pizzas=[pizza.to_dict() for pizza in Pizza.query.all()]
        return make_response(pizzas, 200)
    
    def post(self): 
        data= request.get_json()
        pizza= Pizza(name=data['name'], ingredients=data['ingredients'])
        db.session.add(pizza)
        db.session.commit()

        return make_response(pizza.to_dict(), 201)
        
    
api.add_resource(Pizzas, '/pizza')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
