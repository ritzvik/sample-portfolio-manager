from user.models import UserProfile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.libs.response import send_200, send_400


class GetUserSerializer(Serializer):
    phone = serializers.CharField(max_length=30)

    def validate(self, data):
        phone = data["phone"]
        user = UserProfile.objects.filter(phone=phone).first()
        if user is None:
            raise serializers.ValidationError("user not found")
        return user

    def to_representation(self, user: UserProfile):
        return {"id": user.id, "name": user.name, "phone": user.phone}

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class CreateUserSerializer(Serializer):
    name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=30)

    def validate(self, data):
        phone = data["phone"]
        user = UserProfile.objects.filter(phone=phone).first()
        if user is not None:
            raise serializers.ValidationError("user already present")
        return data

    def create(self, data):
        return UserProfile.objects.create(name=data["name"], phone=data["phone"])

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class UserInfo(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "phone", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True
            )
        ]
    )
    def get(self, request):
        q_params = request.query_params
        ser = GetUserSerializer(data=q_params)
        if ser.is_valid(raise_exception=False):
            return send_200(
                data={"data": ser.data}, message="results retrieved successfully"
            )
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "phone": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        data = dict(request.data)
        ser = CreateUserSerializer(data=data)
        if ser.is_valid(raise_exception=False):
            ser.save()
            return send_200(data={"data": {}}, message="user created successfully")
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )
