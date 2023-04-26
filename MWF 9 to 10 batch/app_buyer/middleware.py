from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta
from app_buyer.models import *


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user has an active session
            # Get the session timeout value from settings
        session_timeout = settings.SESSION_COOKIE_AGE

        # Get the last activity time from the session
        last_activity = request.session.get('email')

        # If the last activity time is not set, set it to the current time
        if not last_activity:
            request.session['last_activity'] = datetime.now()
        else:
            # Calculate the time difference between the last activity and the current time
            time_difference = datetime.now() - last_activity

            # If the time difference is greater than the session timeout value, redirect the user
            if time_difference > timedelta(seconds=session_timeout):
                del request.session['last_activity']
                return redirect(reverse('login'))

        # Call the next middleware or view
        response = self.get_response(request)

        # Update the last activity time in the session
        request.session['last_activity'] = datetime.now()

        return response
