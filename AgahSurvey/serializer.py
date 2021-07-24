from rest_framework import serializers
from AgahSurvey.models import Question, Option, Responder


class Brand_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_value', 'option_title']


class Question_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk', 'question_title']


class Responder_fname(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ['responder_name', ]


class Responder_lname(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ['responser_family', ]
