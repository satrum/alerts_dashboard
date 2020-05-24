from django.shortcuts import render

from django.contrib.sessions.models import Session
# Create your views here.

def test(request):
    # Number of visits to this view, as counted in the session variable.
    sessions = Session.objects.all()
    session_count = sessions.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    print(request.session)
    return render(
        request,
        'test.html',
        context={'num_visits': num_visits, 'sessions': sessions, 'session_count': session_count},  # num_visits appended
    )