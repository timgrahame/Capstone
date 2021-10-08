import json
from flask import request, _request_ctx_stack, session, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsnd-tgrahame.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'kongsisland'

# ////////////////////////////////////////////////////////////////////////#
# AuthError Exception
# ////////////////////////////////////////////////////////////////////////#
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# ////////////////////////////////////////////////////////////////////////#
# Get Token Auth Header and split the token.
# ////////////////////////////////////////////////////////////////////////#


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key'
                }, 401)

    bearer_token = auth.split()  # split the token.

    if bearer_token[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Malformed Header.'
        }, 401)

    elif len(bearer_token) == 1 or len(bearer_token) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing Token.'
        }, 403)

    token = bearer_token[1]
    return token

# ////////////////////////////////////////////////////////////////////////#
# Check_permissions(permission, payload) with AuthError checks
# ////////////////////////////////////////////////////////////////////////#


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'No permissions found'
        }, 403)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'You are not Authorized to do this'
        }, 403)
    return True

# ////////////////////////////////////////////////////////////////////////#
# verify_decode_jwt(token)
# ////////////////////////////////////////////////////////////////////////#


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
            }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                                token,
                                rsa_key,
                                algorithms=ALGORITHMS,
                                audience=API_AUDIENCE,
                                issuer='https://' + AUTH0_DOMAIN + '/')
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 403)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description':
                    'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 403)

# ////////////////////////////////////////////////////////////////////////#
# get the token, decode the jwt, validate claims and check the permissions
# ////////////////////////////////////////////////////////////////////////#


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'token' in session:
                token = session['token']
            else:
                token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
