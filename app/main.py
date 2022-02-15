import os

from starlette.applications import Starlette
from starlette.authentication import (
    requires
)
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette_jwt import JWTAuthenticationBackend
from starlette.responses import JSONResponse
from starlette.routing import Route

#
# Default secret pass phrase
#
# Hint, this token is valid up to 2050
#   curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjI1Mjg0NzA0MDN9.rFRL6mWPROc_rsOqwVQbiegi8XQC0Eb9Zb8Jy2Jae44" http://localhost:5555
#
JWT_PASSPHRASE = "MySecretPassPhrase"

if "JWT_PASSPHRASE" in os.environ:
    JWT_PASSPHRASE = os.getenv('JWT_PASSPHRASE')

@requires('authenticated')
async def homepage(request):
    return JSONResponse({'message': 'Welcome home'})

# HTTP 401 when not authenticated
def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({'error': str(exc)}, status_code=401)

routes = [
    Route('/', endpoint=homepage)
]

middleware = [
    Middleware(AuthenticationMiddleware, on_error=on_auth_error, backend=JWTAuthenticationBackend(secret_key=JWT_PASSPHRASE, username_field='sub', options={'verify_aud': False}, algorithm='HS256', prefix='Bearer'))
]

app = Starlette(routes=routes, middleware=middleware)
