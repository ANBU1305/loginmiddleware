from .swagger_schemas import login_request_schema, register_request_body
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@swagger_auto_schema(
    method='post',
    request_body=register_request_body,
    responses={
        201: openapi.Response(
            'User created successfully',
            examples={'application/json': {'token': 'abcd1234'}}
        ),
        400: openapi.Response(
            'Invalid data',
            examples={'application/json': {'error': 'A user with that username already exists.'}}
        )
    },
    operation_description="Register a new user and return an auth token"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        serializer = UserSerializerWithProfile(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response(
            {'error': 'A user with that username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    method='post',
    request_body=login_request_schema,
    responses={
        200: openapi.Response('Login successful', examples={'application/json': {'token': 'abcd1234'}}),
        401: openapi.Response('Invalid credentials', examples={'application/json': {'error': 'Invalid Credentials'}})
    },
    operation_description="Authenticate user and return auth token"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
