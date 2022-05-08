from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(required=False)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)