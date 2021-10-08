import os


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'Io5yicWl61SmWxTZ2S8I8kW_x73X0E-etWyZ10wiACZWqgXJa-A4FP_HS1YtjhTt'
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://tgrah:1234@localhost:5432/kongsisland'

auth0_config = {
    "AUTH0_DOMAIN" : "fsnd-tgrahame.eu.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "kongsisland"
}





