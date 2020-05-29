from django.shortcuts import render, HttpResponse

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
#SessionAuthentication, BasicAuthentication
from rest_framework import permissions
#IsAuthenticated, IsAdminUser


from .models import Category, Poll
from .serializers import CategorySerializer, PollSerializer

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

class PollViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows votes to be viewed or edited.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer



# https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/
class CategoriesView(APIView):
    #authentication_classes = [authentication.SessionAuthentication]
    #permission_classes = [permissions.AllowAny]
    #authentication_classes = [authentication.SessionAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        #request.session['mydata'] = 'data'
        if request.session.get('session_user', None) is None:
            request.session['session_user'] = 'initialized'
        print(request.session.session_key)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'categories': serializer.data, 'user': request.session.get('session_user', None)})

    def post(self, request):
        category = request.data.get("category")
        serializer = CategorySerializer(data=category)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()
        return Response({"success": "Category '{}' created successfully".format(category_saved.name)})


class PollView(APIView):

    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response({'polls': serializer.data})  # headers, status

    def post(self, request):
        poll = request.data.get("poll")
        serializer = PollSerializer(data=poll)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({"success": "Poll '{}' created successfully".format(poll_saved.name)})

def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse(content='cookie created')


from django.contrib.sessions.apps import SessionsConfig
from django.contrib.sessions.backends.db import SessionStore