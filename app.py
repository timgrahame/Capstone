# ---------------------------------------------------------------------------#
# Imports
# ---------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, jsonify, abort
from flask import Flask, session, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from datetime import datetime
import sys
from flask_wtf import Form
from flask_cors import CORS, cross_origin
from werkzeug import datastructures
from authlib.integrations.flask_client import OAuth
from forms import *
from operator import itemgetter
from models import db_drop_and_create_all, setup_db, Zoo, Gorilla, Bookings
from six.moves.urllib.parse import urlencode
from auth import AuthError, requires_auth

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

# ///////////////////////////////////////////////////////////////////////////#
# App Config.
# ///////////////////////////////////////////////////////////////////////////#

def create_app():
    app = Flask(__name__)
    setup_db(app)
    moment = Moment(app)
    app.config.from_object('config')
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    CORS(app)

    # Uncheck comment below to create database with a few entries per table
    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # ---------------------------------------------------------------------------#
    # Filters.
    # ---------------------------------------------------------------------------#

    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "MM, dd, y"
        return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters['datetime'] = format_datetime

    # ---------------------------------------------------------------------------#
    # Auth 0 stuff
    # ---------------------------------------------------------------------------#

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url='https://fsnd-tgrahame.eu.auth0.com' + '/oauth/token',
        authorize_url='https://fsnd-tgrahame.eu.auth0.com' + '/authorize',
        client_kwargs={
            'scope': 'openid profile email'
                }
    )

    @app.route('/')
    @cross_origin()
    def index():
        return render_template('pages/home.html')

    # ---------------------------------------------------------------------------#
    # route handler to log in
    # ---------------------------------------------------------------------------#

    @app.route('/login', methods=['GET'])
    @cross_origin()
    def login():
        print('Audience: {}'.format(AUTH0_AUDIENCE))
        return auth0.authorize_redirect(
          redirect_uri='%s/post-login' % AUTH0_CALLBACK_URL,
          audience=AUTH0_AUDIENCE
        )

    # ---------------------------------------------------------------------------#
    # route handler for home page once logged in
    # ---------------------------------------------------------------------------#

    @app.route('/post-login', methods=['GET'])
    @cross_origin()
    def post_login():
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        print(session['token'])
        return render_template('pages/home.html')

    # ---------------------------------------------------------------------------#
    # route handler to log out
    # ---------------------------------------------------------------------------#

    @app.route('/logout')
    @cross_origin()
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {
            'returnTo': url_for('index', _external=True),
            'client_id': AUTH0_CLIENT_ID}
        return redirect(
            'https://fsnd-tgrahame.eu.auth0.com' +
            '/v2/logout?' + urlencode(params))

    # ///////////////////////////////////////////////////////////////////////////#
    # Zoos
    # ///////////////////////////////////////////////////////////////////////////#

    # ---------------------------------------------------------------------------#
    # generic page listing zoos and upcoming bookings
    # ---------------------------------------------------------------------------#

    @app.route('/zoos')
    @cross_origin()
    @requires_auth('view:zoos')
    def zoos(payload):
        zoos = Zoo.query.all()
        data = []
        now = datetime.now()

        for zoo in zoos:
            bookings = Bookings.query.filter_by(zoo_id=zoo.id).all()
            num_upcoming = 0
            for booking in bookings:
                if booking.start_time > now:
                    num_upcoming += 1
            data.append({
                "id": zoo.id,
                "name": zoo.name +
                        ' (' + str(num_upcoming) +
                        ' upcoming bookings)'
                        })

        return jsonify({
            'success': True,
            'zoos': data,
        }), 200

        # comment above 'return' and uncomment below to return frontend
        # return render_template('pages/zoos.html', zoos=data)

    # ---------------------------------------------------------------------------#
    # search for zoos
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/search', methods=['POST'])
    @requires_auth('view:zoos')
    def search_Zoos(payload):
        search_term = request.form.get('search_term', '')
        Zoosearch = Zoo.query.filter(
            Zoo.name.ilike("%" + search_term + "%")).all()
        if len(Zoosearch) < 1:
            Notfoundstr = "Not found"
            flash("Sorry, we can't find a zoos that matches that criteria")
            response = {
                  "data": [{
                        "count": len(Zoosearch),
                        "name": Notfoundstr,
                        "num_upcoming_bookings": 0,
                        }]
                      }
        else:
            for result in Zoosearch:
                bookingsearch = Bookings.query.filter(
                    Bookings.zoo_id == result.id).count()
                response = {
                  "data": [{
                        "count": len(Zoosearch),
                        "id": result.id,
                        "name": result.name,
                        "num_upcoming_bookings": bookingsearch,
                        } for result in Zoosearch]
                      }
        return jsonify({
              'success': True,
              'results': response,
          }), 200

        # comment above 'return' and uncomment below to return frontend
        # return render_template('pages/search_Zoos.html', /
        # results=response, search_term=request.form.get('search_term', ''))

    # ---------------------------------------------------------------------------#
    # specific zoo endpoint
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/<int:zoo_id>')
    @requires_auth('view:zoos')
    def booking_zoo(payload, zoo_id):

        zoos = Zoo.query.get(zoo_id)
        booking = []
        oldbooking = []
        now = datetime.now()

        upcoming_bookings_count = 0
        future_bookings = db.session.query(Bookings).join(Gorilla).filter(
            Bookings.zoo_id == zoo_id).filter(Bookings.start_time > now).all()
        upcoming_booking = []
        for booking in future_bookings:
            upcoming_bookings_count += 1
            upcoming_booking.append({
              "gorilla_id": booking.gorilla_id,
              "gorilla_name": booking.gorilla.name,
              "gorilla_image_link": booking.gorilla.image_link,
              "start_time": format_datetime(str(booking.start_time))
            })

        past_bookings_count = 0
        old_bookings = db.session.query(Bookings).join(Gorilla).filter(
          Bookings.zoo_id == zoo_id).filter(Bookings.start_time < now).all()
        past_booking = []
        for oldbooking in old_bookings:
            past_bookings_count += 1
            past_booking.append({
                      "gorilla_id": oldbooking.gorilla_id,
                      "gorilla_name": oldbooking.gorilla.name,
                      "gorilla_image_link": oldbooking.gorilla.image_link,
                      "start_time": format_datetime(str(oldbooking.start_time))
                      })
        data = {
          "id": zoo_id,
          "name": zoos.name,
          "address": zoos.address,
          "city": zoos.city,
          "country": zoos.country,
          "phone": zoos.phone,
          "website": zoos.website_link,
          "seeking_animal": zoos.seeking_animal,
          "seeking_description": zoos.seeking_description,
          "past_bookings": past_booking,
          "past_bookings_count": past_bookings_count,
          "upcoming_bookings": upcoming_booking,
          "upcoming_bookings_count": upcoming_bookings_count
          }

        return jsonify({
              'success': True,
              'zoos': data,
          }), 200

        # comment above 'return' and uncomment below to return frontend
        # return render_template('pages/show_zoo.html', zoos=data)

    # ---------------------------------------------------------------------------#
    # open create zoo page
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/create', methods=['GET'])
    @requires_auth('add:zoos')
    def create_zoo_form(payload):
        form = ZooForm()
        return render_template('forms/new_zoo.html', form=form)

    # ---------------------------------------------------------------------------#
    # create new zoo endpoint
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/create', methods=['POST'])
    @requires_auth('add:zoos')
    def create_zoo_submission(payload):
        error = False
        form = ZooForm()
        if form is None:
            abort(404)

        print(form.name.data)
        zoo_name = form.name.data
        zoo_address = form.address.data
        zoo_city = form.city.data
        zoo_country = form.country.data
        zoo_phone = form.phone.data
        zoo_website = form.website_link.data
        zoo_seeking_talent = form.seeking_talent.data
        zoo_seeking_description = form.seeking_description.data
        try:

            create_zoo = Zoo(name=zoo_name,
                             address=zoo_address,
                             city=zoo_city,
                             country=zoo_country,
                             phone=zoo_phone,
                             website_link=zoo_website,
                             seeking_animal=zoo_seeking_talent,
                             seeking_description=zoo_seeking_description
                             )

            create_zoo.zooinsert()

            return jsonify({
              'success': True,
              'name': create_zoo.name
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            flash('Unspecified error.  Zoo  ' + request.form['name'] +
                  ' not added. We are sorry, there was nothing we could do!')
            abort(422)

    # ---------------------------------------------------------------------------#
    # open zoo page for editting
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/<int:zoo_id>/edit', methods=['GET'])
    @cross_origin()
    @requires_auth('modify:zoo')
    def edit_zoo(payload, zoo_id):
        zoos = Zoo.query.first_or_404(zoo_id)
        form = ZooForm(obj=zoos)

        return render_template('forms/edit_zoo.html', form=form, zoos=zoos)

    # ---------------------------------------------------------------------------#
    # edit zoo endpoint
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/<int:zoo_id>/edit', methods=['PATCH'])
    @cross_origin()
    @requires_auth('modify:zoo')
    def edit_zoo_submission(payload, zoo_id):

        try:
            body = request.get_json()
            if body is None:
                abort(404)
            editzoos = Zoo.query.filter(Zoo.id == zoo_id).one_or_none()

            zooname = body.get("name", None)
            if zooname is not None:
                editzoos.name = zooname

            address = body.get("address", None)
            if address is not None:
                editzoos.address = address

            zoocity = body.get("city", None)
            if zoocity is not None:
                editzoos.city = zoocity

            zoocountry = body.get("country", None)
            if zoocountry is not None:
                editzoos.country = zoocountry

            phone = body.get("phone", None)
            if phone is not None:
                editzoos.phone = phone

            zoowebsite = body.get("website", None)
            if zoowebsite is not None:
                editzoos.website = zoowebsite

            seekinganimal = body.get("seeking_animal", None)
            if seekinganimal is not None:
                editzoos.seeking_animal = seekinganimal

            seekingdesc = body.get("seeking_description", None)
            if seekingdesc is not None:
                editzoos.seeking_description = seekingdesc

            editzoos.zooupdate()
            return jsonify({
                'success': True,
                'zoos': editzoos.name
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ---------------------------------------------------------------------------#
    # Delete specific zoo
    # ---------------------------------------------------------------------------#

    @app.route('/zoos/<int:zoo_id>/delete', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:zoos')
    def delete_zoo(payload, zoo_id):

        try:
            deletezoo = Zoo.query.filter(Zoo.id == zoo_id).one_or_none()

            deletezoo.zoodelete()
            return jsonify({
              'success': True,
              'zoo': zoo_id
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ///////////////////////////////////////////////////////////////////////////#
    # Gorillas
    # ///////////////////////////////////////////////////////////////////////////#

    # ---------------------------------------------------------------------------#
    # open generic gorillas page including bookings
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas')
    @cross_origin()
    @requires_auth('view:gorillas')
    def gorillas(payload):

        gorillas = Gorilla.query.all()
        data = []
        now = datetime.now()

        for gorilla in gorillas:
            bookings = Bookings.query.filter_by(gorilla_id=gorilla.id).all()
            num_upcoming = 0
            for booking in bookings:        #
                if booking.start_time > now:
                    num_upcoming += 1

            data.append({
                "id": gorilla.id,
                "name": gorilla.name +
                        ' (' + str(num_upcoming) + ' upcoming bookings)'
                        })

        return jsonify({
              'success': True,
              'gorillas': data,
          }), 200

        # uncomment above 'return' and uncomment below for front end
        # return render_template('pages/gorillas.html', gorillas=data)

    # ---------------------------------------------------------------------------#
    # search for gorillas endpoint
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/search', methods=['POST'])
    @cross_origin()
    @requires_auth('view:gorillas')
    def search_gorillas(payload):
        search_term = request.form.get('search_term', '')
        gorillasearch = Gorilla.query.filter(
                        Gorilla.name.ilike("%" + search_term + "%")).all()
        if len(gorillasearch) < 1:
            Notfoundstr = "Not found"
            flash("Sorry, we can't find any gorillas that match that criteria")
            response = {
                "data": [{
                    "count": len(gorillasearch),
                    "name": Notfoundstr,
                    "num_upcoming_bookings": 0,
                        }]
                      }
        else:
            for result in gorillasearch:
                bookingsearch = Bookings.query.filter(
                      Bookings.gorilla_id == result.id).count()
                response = {
                    "data": [{
                            "count": len(gorillasearch),
                            "id": result.id,
                            "name": result.name,
                            "num_upcoming_bookings": bookingsearch,
                            } for result in gorillasearch]
                          }

        return jsonify({
                'success': True,
                'results': response,
            }), 200

        # uncomment above 'return' and uncomment below for front end
        # return render_template('pages/search_gorillas.html', /
        # results=response, search_term=request.form.get('search_term', ''))

    # ---------------------------------------------------------------------------#
    # open specific gorilla page
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/<int:gorilla_id>')
    @cross_origin()
    @requires_auth('view:gorillas')
    def booking_gorilla(payload, gorilla_id):
        upcoming_bookings = []
        past_bookings = []
        gorilla = Gorilla.query.get(gorilla_id)
        now = datetime.now()
        upcoming_bookings_count = 0
        future_bookings = db.session.query(Bookings).join(Zoo).filter(
                  Bookings.gorilla_id == gorilla_id).filter(
                  Bookings.start_time > now).all()
        upcoming_booking = []
        for booking in future_bookings:
            upcoming_bookings_count += 1
            upcoming_booking.append({
                "zoo_id": booking.zoo_id,
                "zoo_name": booking.zoo.name,
                "start_time": format_datetime(str(booking.start_time))
                      })

        # now look for past bookings to add to gorilla page.

        past_bookings_count = 0
        old_bookings = db.session.query(Bookings).join(Zoo).filter(
                  Bookings.gorilla_id == gorilla_id).filter(
                  Bookings.start_time < now).all()
        past_booking = []
        for oldbooking in old_bookings:
            past_bookings_count += 1
            past_booking.append({
                    "zoo_id": oldbooking.zoo_id,
                    "zoo_name": oldbooking.zoo.name,
                    "start_time": format_datetime(str(oldbooking.start_time))
                    })

        data = {
                  "id": gorilla_id,
                  "name": gorilla.name,
                  "city": gorilla.city,
                  "country": gorilla.country,
                  "phone": gorilla.phone,
                  "website": gorilla.website,
                  "facebook_link": gorilla.facebook_link,
                  "seeking_zoo": gorilla.seeking_zoo,
                  "seeking_description": gorilla.seeking_description,
                  "image_link": gorilla.image_link,
                  "past_bookings": past_booking,
                  "past_bookings_count": past_bookings_count,
                  "upcoming_bookings": upcoming_booking,
                  "upcoming_bookings_count": upcoming_bookings_count
        }
        print(past_booking)

        return jsonify({
            'success': True,
            'gorilla': data,
            }), 200

        # uncomment above 'return' and uncomment below for front end
        # return render_template('pages/show_gorilla.html', gorilla=data)

    # ---------------------------------------------------------------------------#
    #  open specific gorilla page ready for editing
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/<int:gorilla_id>/edit', methods=['GET'])
    @cross_origin()
    @requires_auth('modify:gorilla')
    def edit_gorilla(payload, gorilla_id):
        gorilla = Gorilla.query.get(gorilla_id)
        form = GorillaForm(obj=gorilla)
        gorilla = {
                "id": gorilla_id,
                "name": gorilla.name,
                "city": gorilla.city,
                "country": gorilla.country,
                "phone": gorilla.phone,
                "website": gorilla.website,
                "seeking_zoo": gorilla.seeking_zoo,
                "seeking_description": gorilla.seeking_description,
                "image_link": gorilla.image_link,
        }
        return render_template(
            'forms/edit_gorilla.html',
            form=form, gorilla=gorilla)

    # ---------------------------------------------------------------------------#
    # Edit Gorilla
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/<int:gorilla_id>/edit', methods=['PATCH'])
    @cross_origin()
    @requires_auth('modify:gorilla')
    def edit_gorilla_submission(payload, gorilla_id):

        try:
            body = request.get_json()
            if body is None:
                abort(404)
            editgorilla = Gorilla.query.filter(
                      Gorilla.id == gorilla_id).one_or_none()

            gorillaname = body.get("name", None)
            if gorillaname is not None:
                editgorilla.name = gorillaname

            gorillacity = body.get("city", None)
            if gorillacity is not None:
                editgorilla.city = gorillacity

            gorillacountry = body.get("country", None)
            if gorillacountry is not None:
                editgorilla.country = gorillacountry

            gorillaphone = body.get("phone", None)
            if gorillaphone is not None:
                editgorilla.phone = gorillaphone

            gorillalink = body.get("website_link", None)
            if gorillalink is not None:
                editgorilla.website = gorillalink

            gorillaseek = body.get("seeking_zoo", None)
            if gorillaseek is not None:
                editgorilla.seeking_zoo = gorillaseek

            gorillaseekdesc = body.get("seeking_description", None)
            if gorillaseekdesc is not None:
                editgorilla.seeking_description = gorillaseekdesc

            editgorilla.gorillaupdate()

            return jsonify({
              'success': True,
              'gorilla': editgorilla.name
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ---------------------------------------------------------------------------#
    # Get add Gorilla page
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/create', methods=['GET'])
    @cross_origin()
    @requires_auth('add:gorillas')
    def create_gorilla_form(payload):
        form = GorillaForm()
        return render_template('forms/new_gorilla.html', form=form)

    @app.route('/gorillas/create', methods=['POST'])
    @cross_origin()
    @requires_auth('add:gorillas')
    def create_gorilla_submission(payload):
        error = False
        form = GorillaForm()
        if form is None:
            abort(404)

        gorilla_name = form.name.data
        gorilla_city = form.city.data
        gorilla_country = form.country.data
        gorilla_phone = form.phone.data
        gorilla_website = form.website_link.data
        gorilla_seeking_zoo = form.seeking_zoo.data
        gorilla_seeking_description = form.seeking_description.data
        gorilla_image = form.image_link.data
        try:

            create_gorilla = Gorilla(
                            name=gorilla_name,
                            city=gorilla_city,
                            country=gorilla_country,
                            phone=gorilla_phone,
                            website=gorilla_website,
                            seeking_zoo=gorilla_seeking_zoo,
                            seeking_description=gorilla_seeking_description,
                            image_link=gorilla_image
                            )

            create_gorilla.gorillainsert()

            return jsonify({
              'success': True,
              'name': create_gorilla.name
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ---------------------------------------------------------------------------#
    # Delete Gorilla
    # ---------------------------------------------------------------------------#

    @app.route('/gorillas/<int:gorilla_id>/delete', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:gorillas')
    def delete_gorilla(payload, gorilla_id):

        try:
            deletegorilla = Gorilla.query.filter(
                Gorilla.id == gorilla_id).one_or_none()

            deletegorilla.gorilladelete()
            return jsonify({
              'success': True,
              'gorilla': gorilla_id
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ///////////////////////////////////////////////////////////////////////////#
    # Bookings
    # ///////////////////////////////////////////////////////////////////////////#

    # ---------------------------------------------------------------------------#
    # View Bookings page
    # ---------------------------------------------------------------------------#

    @app.route('/bookings')
    @cross_origin()
    @requires_auth('view:bookings')
    def bookings():

        data = []

        bookings = Bookings.query.all()

        for booking in bookings:
            bookingszooid = booking.zoo_id
            bookingsgorillaid = booking.gorilla_id
            starttime = booking.start_time

            bookings = db.session.query(Bookings).join(Zoo).all()

            for booking in bookings:
                data.append({
                          "zoo_id": booking.zoo_id,
                          "zoo_name": booking.zoo.name,
                          "gorilla_id":  booking.gorilla_id,
                          "gorilla_name": booking.gorilla.name,
                          "gorilla_image_link": booking.gorilla.image_link,
                          "start_time": str(starttime)
                            })

        return jsonify({
            'success': True,
            'bookings': data,
            }), 200

        # uncomment above 'return' and uncomment below for front end
        # return render_template('pages/bookings.html', bookings=data)

    # ---------------------------------------------------------------------------#
    # Open Create Bookings page
    # ---------------------------------------------------------------------------#

    @app.route('/bookings/create')
    @cross_origin()
    @requires_auth('add:bookings')
    def create_bookings(payload):
        # renders form. do not touch.
        form = BookingForm()
        return render_template('forms/new_booking.html', form=form)

    # ---------------------------------------------------------------------------#
    # Post New Booking
    # ---------------------------------------------------------------------------#

    @app.route('/bookings/create', methods=['POST'])
    @cross_origin()
    @requires_auth('add:bookings')
    def create_booking_submission(payload):

        form = BookingForm()
        if form is None:
            abort(404)

        gorillas_id = form.gorilla_id.data
        zoos_id = form.zoo_id.data
        visit_info = form.start_time.data

        try:
            create_booking = Bookings(
                            gorilla_id=gorillas_id,
                            zoo_id=zoos_id,
                            start_time=visit_info)

            create_booking.bookinginsert()

            return jsonify({
              'success': True,
              'booking': create_booking.start_time
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ---------------------------------------------------------------------------#
    # Delete Booking
    # ---------------------------------------------------------------------------#

    @app.route('/bookings/<int:booking_id>/delete', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:bookings')
    def delete_booking(payload, booking_id):

        try:
            deletebooking = Bookings.query.filter(
                Bookings.id == booking_id).one_or_none()
            deletebooking.bookingdelete()

            return jsonify({
              'success': True,
              'bookingdelete': booking_id
            }), 200

        except Exception as e:
            print("Exception is", e)
            error = True
            abort(422)

    # ///////////////////////////////////////////////////////////////////////////#
    # Error Handlers
    # ///////////////////////////////////////////////////////////////////////////#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable error - does the entity exist?"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error - The server wants to be awkward"
        }), 500

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "You need to be logged in to view this page"
        }), 400

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    # ---------------------------------------------------------------------------#
    # Auth Error Handler
    # ---------------------------------------------------------------------------#

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.error["code"],
            "message": error.error["description"]
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
