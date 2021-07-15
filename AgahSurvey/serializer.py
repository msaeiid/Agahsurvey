from rest_framework import serializers
from AgahSurvey.models import Brand, Question


class Brand_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['pk', 'title', 'image']


class Question_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk','question_title']
