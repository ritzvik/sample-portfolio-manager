from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.constants.stashaway_constants import SchemeTypes
from code_service.libs.response import send_200, send_400
from stashaway.models import Scheme


class CreatSchemeSerializer(Serializer):
    name = serializers.CharField(max_length=200)
    scheme_type = serializers.ChoiceField(choices=[t.value for t in SchemeTypes])

    def create(self, data):
        return Scheme.objects.create(name=data["name"], scheme_type=data["scheme_type"])

    def to_representation(self, scheme: Scheme):
        return {
            "id": scheme.id,
            "name": scheme.name,
            "scheme_type": scheme.scheme_type,
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class SchemeInfo(APIView):
    def get(self, request):
        """
        Get details of all schemes present in the system
        """
        schemes = Scheme.objects.all()
        return send_200(
            {
                "data": [
                    {
                        "id": scheme.id,
                        "name": scheme.name,
                        "scheme_type": scheme.scheme_type,
                    }
                    for scheme in schemes
                ]
            },
            message="schemes retrieved successfully",
        )

    @swagger_auto_schema(request_body=CreatSchemeSerializer)
    def post(self, request):
        """
        Register new schemes in the system
        """
        data = dict(request.data)
        ser = CreatSchemeSerializer(data=data)
        if ser.is_valid(raise_exception=False):
            ser.save()
            return send_200(
                data={"data": ser.data}, message="scheme created successfully"
            )
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )
