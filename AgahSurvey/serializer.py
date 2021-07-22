from rest_framework import serializers
from AgahSurvey.models import Question, Option


class Brand_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_value', 'option_title']


class Question_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk','question_title']
