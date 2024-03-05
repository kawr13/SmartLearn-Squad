from rest_framework import serializers


class UsersSendSerializer(serializers.Serializer):
    users = serializers.