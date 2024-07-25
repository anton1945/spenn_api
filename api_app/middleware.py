from django.conf import settings
from django.utils import timezone
from datetime import datetime,timedelta

class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #Get the current time
        now = timezone.now()

        # Get the last activity time from the session
        last_activity = request.session.get('last_activity')

        if last_activity:
             # Convert the last activity string back to a datetime object
            last_activity = datetime.fromisoformat(last_activity)
            # Calculate the session idle duration
            idle_duration = now - last_activity
            # Check if the session has expired
            if idle_duration > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                # Log out the user and clear the session
                from django.contrib.auth import logout
                logout(request)
                request.session.flush()

        # Update the last activity time in the session
        request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response