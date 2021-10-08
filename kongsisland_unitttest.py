import os
from os import environ as env
import unittest
import flask_testing
import json
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from flask import abort
from models import setup_db, Zoo, Gorilla, Bookings
from app import create_app
import sys


class KongsislandsTestCase(unittest.TestCase):

    # -------------------------------------------------------------------------------#
    # Prepare Database
    # -------------------------------------------------------------------------------#

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "kongsisland"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
                            env['DB_USER'],
                            env['DB_PASSWORD'],
                            env['DB_HOST'],
                            env['DB_NAME']
                            )
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        # -------------------------------------------------------------------------------#
        # Get Tokens
        # -------------------------------------------------------------------------------#

        self.vet_token = {
            "Authorization": "Bearer {}".format(
                    os.environ.get('VET_TOKEN'))}
        self.zookeeper_token = {
            "Authorization": "Bearer {}".format(
                    os.environ.get('ZOOKEEPER_TOKEN'))}
        self.zoodirector_token = {
            "Authorization": "Bearer {}".format(
                    os.environ.get('ZOODIRECTOR_TOKEN'))}

        # -------------------------------------------------------------------------------#
        # Create Test data
        # -------------------------------------------------------------------------------#

        self.test_zoo_add = {
            "name": "Berlins Zoo",
            "city": "Berlin",
            "country": "DE",
            "address":
                "Zoologischer Garten Berlin AG Hardenbergplatz 8 10787 Berlin",
            "phone": "+49 30 254011",
            "website_link": "https://www.zoo-berlin.de/en",
            "seeking_animal": 1,
            "seeking_description": "It has been too successful"
        }

        self.test_zoo_chg = {
            "name": "Berlin Zoo",
            "city": "Berlin",
            "country": "DE",
            "address":
                "Zoologischer Garten Berlin AG Hardenbergplatz 8 10787 Berlin",
            "phone": "+49 30 254011",
            "website_link": "https://www.zoo-berlin.de/en",
            "seeking_animal": 1,
            "seeking_description": "It has been too successful"
        }

        self.test_gorilla_add = {
            "name": "Gorgeous George",
            "city": "Berlin",
            "country": "DE",
            "phone": "+49 30 254011",
            "website_link": "https://www.zoo-berlin.de/en",
            "seeking_zoo": 1,
            "seeking_description": "George is ready for his next posting",
            "image_link":
            "https://static.standard.co.uk/s3fs-public/ \
                thumbnails/image/2016/05/30/20/dublinzoo.jpg"
        }

        self.test_gorilla_chg = {
            "name": "Gorgeous George III",
            "city": "Berlin",
            "country": "DE",
            "phone": "+49 30 254011",
            "website_link": "https://www.zoo-berlin.de/en",
            "seeking_zoo": 1,
            "seeking_description": "George is ready for his next posting",
            "image_link": "https://static.standard.co.uk/ \
                s3fs-public/thumbnails/image/2016/05/30/20/dublinzoo.jpg"
        }

        self.test_bookings_add = {
            "gorilla_id": 2,
            "zoo_id": 2,
            "start_time": "2024-01-01 12:00:00"}

    # ------------------------------------------------------------------------#
    # Tear down conditions (Pass)
    # ------------------------------------------------------------------------#

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ////////////////////////////////////////////////////////////////////////#
    # Test No Auth key
    # ////////////////////////////////////////////////////////////////////////#

    def testa1_zoos_fail(self):
        res = self.client().get('/zoos')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa2_zoos_page_fail(self):
        res = self.client().get('/zoos/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa3_gorillas_fail(self):
        res = self.client().get('/gorillas')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa4_gorillas_page_fail(self):
        res = self.client().get('/gorillas/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa5_zoos_create_fail(self):
        res = self.client().post('/zoos/create', json=self.test_zoo_add)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa6_zoos_amend_fail(self):
        res = self.client().patch('/zoos/1/edit', json=self.test_zoo_chg)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa7_zoos_delete_fail(self):
        res = self.client().delete('/zoos/1/delete')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa8_gorillas_create_fail(self):
        res = self.client().post('/gorillas/create',
                                 json=self.test_gorilla_add)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testa9_gorillas_amend_fail(self):
        res = self.client().patch('/gorillas/1/edit',
                                  json=self.test_gorilla_chg)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testb1_gorillas_delete_fail(self):
        res = self.client().delete('/gorillas/1/delete')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testb2_bookings_create_fail(self):
        res = self.client().post('/bookings/create',
                                 json=self.test_bookings_add)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    def testb3_bookings_create_fail(self):
        res = self.client().delete('/bookings/1/delete')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to find the appropriate key')

    # ////////////////////////////////////////////////////////////////////////#
    # Test Zoo Keeper User
    # ////////////////////////////////////////////////////////////////////////#

    def testb4_zookeeper_zoos_pass(self):
        res = self.client().get('/zoos', headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testb5_zookeper_zoos_page_pass(self):
        res = self.client().get('/zoos/1', headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testb6_zookeeper_gorillas_pass(self):
        res = self.client().get('/gorillas', headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testb7_zookeeper_gorillas_page_pass(self):
        res = self.client().get('/gorillas/1', headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testb8_zookeeper_zoos_create_fail(self):
        res = self.client().post('/zoos/create', json=self.test_zoo_add,
                                 headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testb9_zookeeper_zoos_amend_fail(self):
        res = self.client().patch('/zoos/1/edit', json=self.test_zoo_chg,
                                  headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc1_zookeeper_zoos_delete_fail(self):
        res = self.client().delete('/zoos/1/delete',
                                   headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc2_zookeeper_gorillas_create_fail(self):
        res = self.client().post('/gorillas/create',
                                 json=self.test_gorilla_add,
                                 headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc3_zookeeper_gorillas_amend_fail(self):
        res = self.client().patch('/gorillas/1/edit',
                                  json=self.test_gorilla_chg,
                                  headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc4_zookeeper_gorillas_delete_fail(self):
        res = self.client().delete('/gorillas/1/delete',
                                   headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc5_zookeeper_bookings_create_fail(self):
        res = self.client().post('/bookings/create',
                                 json=self.test_bookings_add,
                                 headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def testc6_zookeeper_bookings_create_fail(self):
        res = self.client().delete('/bookings/1/delete',
                                   headers=self.zookeeper_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    # ////////////////////////////////////////////////////////////////////////#
    # Test Vet User
    # ////////////////////////////////////////////////////////////////////////#

    def testc7_zoos_vet_pass(self):
        res = self.client().get('/zoos', headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testc8_zoos_vet_pass(self):
        res = self.client().get('/zoos', headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testc9_zoos_page_vet_pass(self):
        res = self.client().get('/zoos/1', headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd1_gorillas_vet_pass(self):
        res = self.client().get('/gorillas', headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd2_gorillas_vet_page_pass(self):
        res = self.client().get('/gorillas/1', headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd3_zoos_create_vet_pass(self):
        res = self.client().post('/zoos/create',
                                 json=self.test_zoo_add,
                                 headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd4_zoos_amend_vet_pass(self):
        res = self.client().patch('/zoos/1/edit',
                                  json=self.test_zoo_chg,
                                  headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd5_zoos_delete_vet_pass(self):
        res = self.client().delete('/zoos/1/delete',
                                   headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd6_gorillas_create_vet_pass(self):
        res = self.client().post('/gorillas/create',
                                 json=self.test_gorilla_add,
                                 headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd7_gorillas_amend_vet_pass(self):
        res = self.client().patch('/gorillas/1/edit',
                                  json=self.test_gorilla_chg,
                                  headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd8_gorillas_delete_vet_pass(self):
        res = self.client().delete('/gorillas/1/delete',
                                   headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testd9_bookings_create_vet_fail(self):
        res = self.client().post('/bookings/create',
                                 json=self.test_bookings_add,
                                 headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    def teste1_bookings_create_vet_fail(self):
        res = self.client().delete('/bookings/1/delete',
                                   headers=self.vet_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'You are not Authorized to do this')

    # ////////////////////////////////////////////////////////////////////////#
    # Test Zoo Director User
    # ////////////////////////////////////////////////////////////////////////#

    def teste2_zoodirect_zoos_pass(self):

        res = self.client().get('/zoos', headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste3_zoodirect_zoos_pass(self):
        res = self.client().get('/zoos', headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste4_zoodirect_zoos_page_pass(self):
        res = self.client().get('/zoos/2', headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste5_zoodirect_gorillas_pass(self):
        res = self.client().get('/gorillas', headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste6_zoodirect_gorillas_page_pass(self):
        res = self.client().get('/gorillas/2', headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste7_zoodirect_zoos_create_pass(self):
        res = self.client().post('/zoos/create',
                                 json=self.test_zoo_add,
                                 headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste8_zoodirect_zoos_amend_pass(self):
        res = self.client().patch('/zoos/3/edit',
                                  json=self.test_zoo_chg,
                                  headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def teste9_zoodirect_zoos_delete_pass(self):
        res = self.client().delete('/zoos/3/delete',
                                   headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testf1_zoodirect_gorillas_create_pass(self):
        res = self.client().post('/gorillas/create',
                                 json=self.test_gorilla_add,
                                 headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testf2_zoodirect_gorillas_amend_pass(self):
        res = self.client().patch('/gorillas/3/edit',
                                  json=self.test_gorilla_chg,
                                  headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testf3_zoodirect_gorillas_delete_pass(self):
        res = self.client().delete('/gorillas/3/delete',
                                   headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testf4_zoodirect_bookings_create_pass(self):
        res = self.client().post('/bookings/create',
                                 json=self.test_bookings_add,
                                 headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def testf5_zoodirect_bookings_create_pass(self):
        res = self.client().delete('/bookings/1/delete',
                                   headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ///////////////////////////////////////////////////////////////////////////////#
    # Generic Tests
    # ///////////////////////////////////////////////////////////////////////////////#

    def test_gorillas_delete_nonexistent(self):
        res = self.client().delete('/gorillas/34/delete',
                                   headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'unprocessable error - does the entity exist?')

    def test_zoos_delete_nonexistent(self):
        res = self.client().delete('/zoos/34/delete',
                                   headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'unprocessable error - does the entity exist?')

    def test_zoodirect_zoos_amend_nonexistent(self):
        res = self.client().patch('/zoos/34/edit',
                                  json=self.test_zoo_chg,
                                  headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'unprocessable error - does the entity exist?')

    def test_zoodirect_zoos_amend_nonexistent(self):
        res = self.client().patch('/gorillas/34/edit',
                                  json=self.test_zoo_chg,
                                  headers=self.zoodirector_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],
                         'unprocessable error - does the entity exist?')

# ///////////////////////////////////////////////////////////////////////////////#
# Make the tests conveniently executable
# ///////////////////////////////////////////////////////////////////////////////#


if __name__ == "__main__":
    unittest.main()
