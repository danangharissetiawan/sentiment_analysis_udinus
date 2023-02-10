from rest_framework import serializers
from .models import Broadcast


class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = ['name', 'email', 'message', 'classification']

    def create(self, validated_data):
        return Broadcast.objects.create(**validated_data)