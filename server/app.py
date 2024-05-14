#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, WaterThing, UnderSeaHouse # ADD OTHER MODELS HERE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)


# ROUTES


@app.get('/')
def index():
    return { "stuff": "I am stuff" }, 404

@app.post('/water-things')
def post_rqst():
    new_water_thing = WaterThing(name=request.json['name'], species=request.json['species'])
    db.session.add(new_water_thing)
    db.session.commit()
    return new_water_thing.to_dict(), 201

@app.get('/water-things')
def get_rqst():
    return [wt.to_dict() for wt in WaterThing.query.all()]

@app.get('/water-things/<int:id>')
def get_by_id(id):
    water_thing = WaterThing.query.where(WaterThing.id == id).first()
    if water_thing:
        return water_thing.to_dict(), 200
    else:
        return {"error": "Not found"}, 404

@app.delete("/water-things/<int:id>")
def delete_rqst(id:int):
    water_thing = WaterThing.query.where(WaterThing.id == id).first()

    if water_thing:
        db.session.delete(water_thing)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "Not found"}, 404
    
@app.patch("/water-things/<int:id>")
def patch_rqst(id:int):
    water_thing = WaterThing.query.where(WaterThing.id == id).first()
    if water_thing:
        for key in request.json.keys():
            if not key == "id":
                setattr(water_thing, key, request.json[key])

        db.session.add(water_thing)
        db.session.commit()

        return water_thing.to_dict(), 202
    
    else:
        return {"error": "Not found"}, 404
    
@app.post('/under-sea-house')
def under_sea_post():
    new_under_sea_house = UnderSeaHouse(type=request.json['type'], comfort=request.json['comfort'])
    db.session.add(new_under_sea_house)
    db.session.commit()
    return new_under_sea_house.to_dict(), 201

@app.get('/under-sea-house')
def under_sea_get():
    return [us.to_dict() for us in UnderSeaHouse.query.all()]

@app.get('/under-sea-house/<int:id>')
def under_sea_get_by_id(id):
    sea_house = UnderSeaHouse.query.where(UnderSeaHouse.id == id).first()
    if sea_house:
        return sea_house.to_dict(), 200
    else:
        return {"error": "Not found"}, 404

# APP RUN

if __name__ == '__main__':
    app.run(port=5555, debug=True)
