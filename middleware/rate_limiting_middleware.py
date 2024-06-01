import time
from django.http import JsonResponse
from django.core.cache import cache


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5  # requests
        self.time_window = 60  # seconds

    def __call__(self, request):
        print('🚀 RATE LIMITING MIDDLEWARE CALLED..')

        # LOGIC
        ip_address = self.get_ip_addr(request)
        if not ip_address:
            return JsonResponse({'error': 'Unable to identify client IP address'}, status=400)

        print('IP: ', ip_address)
        # Retrieving from cache
        cache_key = f'rate_limit_{ip_address}'
        request_count, first_request_time = cache.get(
            cache_key, (0, time.time()))

        current_time = time.time()  # Get the current time
        # If the time window has passed, reset the request count and timestamp
        # Else continue
        if current_time - first_request_time > self.time_window:
            request_count = 0
            first_request_time = current_time

        if request_count < self.rate_limit:
            # If the request count is within the limit, increment the count
            request_count += 1
            # Update the cache with the new request count and timestamp
            cache.set(cache_key, (request_count, first_request_time),
                      timeout=self.time_window)
            # Process the request and get the response
            response = self.get_response(request)
        else:
            # If the rate limit is exceeded, return a "Too many requests" error response
            response = JsonResponse({'error': 'Too many requests'}, status=429)

        return response

    def get_ip_addr(self, request):
        x_forwarded_for_addr = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_addr:
            ip = x_forwarded_for_addr  # String Manipulation IF NEEDED
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
