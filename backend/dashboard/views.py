from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.contrib.sessions.models import Session
from django.contrib.sessions.apps import SessionsConfig
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from rest_framework import authentication
#SessionAuthentication, BasicAuthentication

from rest_framework import permissions
#IsAuthenticated, IsAdminUser


from .models import Category, Poll, Results
from .serializers import CategorySerializer, PollSerializer, ResultSerializer

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

def get_cookies(request):
    print(request.COOKIES)
    print(request.headers)
    if request.session.session_key is None:
        request.session['stage']='getcookie'
    if request.session.get('ip', None) is None:
        request.session['ip'] = request.META.get('REMOTE_ADDR', None)

    #response = HttpResponse('ok')
    response = JsonResponse({})
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Origin'] = '*'
    print('new session key: {}'.format(request.session.session_key))
    return response

# [DEPRECATED]
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows votes to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# [DEPRECATED]
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
        print(request.COOKIES)
        #request.session['mydata'] = 'data'
        #for k,v in request.META.items():
        #    print(k,v)
        print(request.headers)
        if request.session.get('ip', None) is None:
            request.session['ip'] = request.META.get('REMOTE_ADDR', None)
        print(request.session.session_key)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        '''
        res.set('Access-Control-Allow-Origin', '*')
        res.set('Access-Control-Allow-Credentials', 'true')
        '''

        return Response({'categories': serializer.data})#, 'user': request.session.get('ip', None)})

    def post(self, request):
        category = request.data.get("category")
        serializer = CategorySerializer(data=category)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()
        return Response({"success": "Category '{}' created successfully".format(category_saved.name)})


class PollView(APIView):

    def get(self, request, format=None):
        print(request.COOKIES)
        print(request.headers)
        print(request.session.session_key)

        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            polls = Poll.objects.filter(category=category_id)
        else:
            polls = Poll.objects.all()

        #polls = Poll.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(polls, request)
        serializer = PollSerializer(result_page, many=True, context={'request': request})
        return Response({'polls': serializer.data}, status=HTTP_200_OK)
    '''
    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response({'polls': serializer.data})  # headers, status
    '''

    def post(self, request):
        poll = request.data.get("poll")
        serializer = PollSerializer(data=poll)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({"success": "Poll '{}' created successfully".format(poll_saved.text)})

class ResultsView(APIView):
    """
    1. проверить наличие session
    2. Results.objects.filter(session_key = session_key)
    3. Если фильтр по poll.pk то его добавить в фильтр
    """

    def get(self, request):
        # check session_key
        session_key = request.session.session_key
        print(session_key)
        if session_key is None:
            return Response({'error': 'need sessionid in cookies'}, HTTP_401_UNAUTHORIZED)

        # check poll_id
        # results = Results.objects.all()
        poll_id = self.request.query_params.get('poll_id', None)
        if poll_id is not None:
            results = Results.objects.filter(poll=poll_id, session_key=session_key)
        else:
            results = Results.objects.filter(session_key=session_key)

        serializer = ResultSerializer(results, many=True)
        return Response({'results': serializer.data, 'poll': poll_id, 'session_key': session_key})  # headers, status

    def post(self, request):
        # check "result" key
        result = request.data.get("result", None)
        if result is None:
            return Response({'error': 'need result key'}, HTTP_400_BAD_REQUEST)

        # check and add session_key
        session_key = request.session.session_key
        print(session_key)
        if session_key is None:
            return Response({'error': 'need sessionid in cookies'}, HTTP_401_UNAUTHORIZED)
        result['session_key'] = session_key
        print(result)

        #validate
        serializer = ResultSerializer(data=result)
        if serializer.is_valid(raise_exception=True):
            # check  Poll.options/Poll.type = Result.result
            print(serializer.validated_data)
            poll = Poll.objects.get(pk=result['poll'])
            print(poll.type, poll.options, result['result'])

            if poll.type == 'A' and poll.options != result['result']:
                return Response({'error': 'incorrect result for poll type A'}, HTTP_400_BAD_REQUEST)
            if poll.type == 'O':
                if len(result['result'])!=1:
                    return Response({'error': 'poll type O, need only 1 result from list'}, HTTP_400_BAD_REQUEST)
                elif result['result'][0] not in poll.options:
                    return Response({'error': 'poll type O, need result from {}'.format(','.join(poll.options))}, HTTP_400_BAD_REQUEST)
            if poll.type == 'M':
                for item in result['result']:
                    if item not in poll.options:
                        return Response({'error': 'poll type M, need one or many results from {}'.format(','.join(poll.options))}, HTTP_400_BAD_REQUEST)

            # check Poll.repeat/repeat_pause (get last result with Poll.)
            old_result = Results.objects.filter(session_key=session_key, poll=result['poll']).first()
            if old_result is not None:
                if not poll.repeat:
                    return Response({'error': 'cannot repeat this poll_id {}, old result_id {}'.format(poll.pk, old_result.pk)}, HTTP_400_BAD_REQUEST)
                else:
                    print('now:\n{} delta:{}\nold:\n{}\nrepeat after:\n{}'.format(timezone.now(),
                                                                             poll.repeat_pause,
                                                                             old_result.created_time,
                                                                             old_result.created_time+poll.repeat_pause))
                    if timezone.now() < old_result.created_time+poll.repeat_pause:
                        return Response({'error': 'cannot repeat this poll_id {}, old result_id {}'.format(poll.pk, old_result.pk)}, HTTP_400_BAD_REQUEST)


            #return Response("good")
            result_saved = serializer.save()
            return Response({"success": "Result '{}' created successfully".format(result_saved)})

def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse(content='cookie created')


class PollstatsView(APIView):
    def get(self, request):

        # check poll_id
        poll_id = self.request.query_params.get('poll_id', None)
        if poll_id is None:
            return Response({'error': 'need /?poll_id=x'}, HTTP_400_BAD_REQUEST)
        print(poll_id)
        try:
            poll = Poll.objects.get(pk=poll_id)
            print(poll)
        except Exception as e:
            return Response({'error': 'exception: {}'.format(str(e))}, HTTP_400_BAD_REQUEST)


        count = Results.objects.filter(poll=poll_id).count()
        print(count)

        return Response({"data": [], "count": count, "poll": poll_id}, status=HTTP_200_OK)

