from rest_framework import serializers
from AgahSurvey.models import Brand


class Brand_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['pk', 'title', 'image']
