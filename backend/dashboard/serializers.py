from .models import Category, Poll, Results
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',  'name', 'visible']

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'text', 'type', 'options', 'another', 'another_text', 'share_text', 'category', 'state', 'created_time', 'color']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['id', 'created_time', 'poll', 'result', 'input_text', 'user', 'session_key']