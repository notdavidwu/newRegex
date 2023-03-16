from mark.models import Text
from rest_framework import serializers

class TextSerializer(serializers.ModelSerializer):
     class Meta:
         model = Text
         fields = '__all__'