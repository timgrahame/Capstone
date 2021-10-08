import os
from os import environ as env
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv
from flask_migrate import Migrate

# load database environment details from .env

load_dotenv()

database_path = 'postgres://ozgxqlvtznemxe:fe85babc7a4a83cbc65752171d5fda988ee5f6181d5519a568a24056a629853e@ec2-23-21-4-7.compute-1.amazonaws.com:5432/d6osfi0qp10auf'

# Below is the local database path

#database_path = "postgresql://{}:{}@{}/{}".format(
#    env['DB_USER'],
#    env['DB_PASSWORD'],
#    env['DB_HOST'],
#    env['DB_NAME']
#    )

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    print("Database dropped")
    db.create_all()
    print("Database created")

        # add demo rows for zoo which is helping testing
    zoo = Zoo(
        name ='London Zoo',
        city ='London',
        country ='UK',
        address ='Regents Park London NW1 4RY',
        phone ='+44 0 344 225 1826',
        website_link = 'https://www.zsl.org/zsl-london-zoo',
        seeking_animal = True,
        seeking_description = 'Any adult silverback')
    zoo.zooinsert()

    gorilla = Gorilla(
        name = 'George',
        city = 'San Fransisco',
        country = 'USA',
        phone = '+1(415) 753-7080',
        image_link = 'https://www.publicdomainpictures.net/pictures/90000/velka/silverback-gorilla-1402593801MmY.jpg',
        website = 'https://www.sfzoo.org/',
        facebook_link = 'https://www.facebook.com/sanfranzoo/posts/10158789244098165',
        seeking_zoo = True,
        seeking_description = 'Any Zoo with available females')
    gorilla.gorillainsert()

    booking = Bookings(
        zoo_id = '1',
        gorilla_id = '1',
        start_time = '2021-12-31 12:00')
    booking.bookinginsert()

class Zoo(db.Model):
    __tablename__ = 'Zoo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_animal = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    bookings = db.relationship('Bookings', backref="zoo", lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def zooinsert(self):
        db.session.add(self)
        db.session.commit()
    
    def zooupdate(self):
        db.session.commit()

    def zoodelete(self):
        db.session.delete(self)
        db.session.commit()

class Gorilla(db.Model):
    __tablename__ = 'Gorilla'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_zoo = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    bookings = db.relationship('Bookings', backref="gorilla", lazy=True)

    def gorillainsert(self):
        db.session.add(self)
        db.session.commit()

    def gorillaupdate(self):
        db.session.commit()

    def gorilladelete(self):
        db.session.delete(self)
        db.session.commit()


class Bookings(db.Model):
    __tablename__ = 'Bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zoo_id = db.Column(db.Integer, db.ForeignKey('Zoo.id'))
    gorilla_id = db.Column(db.Integer, db.ForeignKey('Gorilla.id'))
    start_time = db.Column(db.DateTime())

    def bookinginsert(self):
        db.session.add(self)
        db.session.commit()

    def bookingupdate(self):
        db.session.commit()

    def bookingdelete(self):
        db.session.delete(self)
        db.session.commit()
