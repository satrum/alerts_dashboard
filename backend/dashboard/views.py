from django.shortcuts import render

from django.contrib.sessions.models import Session
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Category
from .serializers import CategorySerializer

# Create your views here.

def test(request):
    # Number of visits to this view, as counted in the session variable.
    sessions = Session.objects.all()
    for s in sessions:
        print(s, '\n')
    session_count = sessions.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    s = request.session
    for k,v in s.items():
        print(k, v)
    return render(
        request,
        'test.html',
        context={'num_visits': num_visits, 'sessions': sessions, 'session_count': session_count},  # num_visits appended
    )


# API views
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows votes to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
