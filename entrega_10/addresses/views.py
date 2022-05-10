from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from addresses.models import Addresses
from addresses.serializers import AddressSerializer, CreateAddressSerializer

class AddressView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        serializer = CreateAddressSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        address = Addresses.objects.filter(**serializer.validated_data).first()

        if not address:
            address = Addresses.objects.create(**serializer.validated_data)

        request.user.address = address
        request.user.save()

        newAddress = AddressSerializer(address)

        newAddress = newAddress.data

        return Response( newAddress, 200 )