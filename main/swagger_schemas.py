# authentication_api/swagger_schemas.py

from drf_yasg import openapi
from .serializers import UserLoginSerializer

# Login request body
login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user')
    }
)

# Register request body uses the DRF serializer directly
register_request_body = UserLoginSerializer
