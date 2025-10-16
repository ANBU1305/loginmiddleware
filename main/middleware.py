# authentication_api/middleware.py

import time
import json
import redis
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin

# Connect to Redis
# Adjust the host and port if your Redis server is located elsewhere
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    redis_client = None

class LoginRateLimitMiddleware(MiddlewareMixin):
    MAX_ATTEMPTS = 10
    WINDOW = 60

    def process_request(self, request):
        if not redis_client:
            # If Redis connection failed, fall back to no rate limiting or an error response
            # For this example, we'll simply pass the request through.
            return None

        # Check if the path is the login endpoint and the method is POST
        if request.path == '/api/login/' and request.method == 'POST':
            
            username = None
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                    username = data.get('username')
                except (json.JSONDecodeError, AttributeError):
                    return HttpResponseBadRequest("Invalid request format.")
            else:
                username = request.POST.get('username')

            if not username:
                return None

            # Use Redis key to store attempts for this user
            key = f"rate_limit:{username}"
            now = time.time()

            # Use a Redis pipeline for atomic operations
            pipe = redis_client.pipeline()
            
            # LPUSH: Add the current timestamp to the start of the list
            pipe.lpush(key, now)
            
            # LTRIM: Keep only the latest `MAX_ATTEMPTS` entries
            pipe.ltrim(key, 0, self.MAX_ATTEMPTS - 1)
            
            # Set an expiration for the key to clear old data
            pipe.expire(key, self.WINDOW)

            # Execute all commands in the pipeline
            pipe.execute()

            # Get the current number of attempts
            attempts_count = redis_client.llen(key)
            print("attempts_count",attempts_count)

            if attempts_count >= self.MAX_ATTEMPTS:
                return JsonResponse(
                    {'error': 'Too many login attempts. Please try again later.'},
                    status=429
                )

        return None