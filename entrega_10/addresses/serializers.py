from rest_framework import serializers

from users.serializers import UserSerializer

class CreateAddressSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()

class AddressSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()
    
    users = UserSerializer(many=True)