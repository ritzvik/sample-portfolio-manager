from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.libs.response import send_200, send_400
from code_service.validators import uuid_validator
from stashaway.models import MonthlyRecurringDepositSchedule, Portfolio


class _CreateScheduleSerializer(Serializer):
    portfolio_id = serializers.CharField(validators=(uuid_validator,))
    day_of_month = serializers.IntegerField(min_value=1, max_value=28)

    def validate(self, data):
        portfolio = Portfolio.objects.filter(id=data["portfolio_id"]).first()
        if portfolio is None:
            raise serializers.ValidationError("No portfolio with this ID exists")
        return data

    def create(self, data):
        return MonthlyRecurringDepositSchedule.objects.update_or_create(
            portfolio_id=data["portfolio_id"],
            defaults={"day_of_month": data["day_of_month"]},
        )[0]

    def to_representation(self, schedule: MonthlyRecurringDepositSchedule):
        return {
            "portfolio_id": schedule.portfolio_id,
            "day_of_month": schedule.day_of_month,
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class RecurringScheduleInfo(APIView):
    @swagger_auto_schema(request_body=_CreateScheduleSerializer)
    def post(self, request):
        """
        Register new monthly deposit schedule for portfolio for user
        """
        data = dict(request.data)
        ser = _CreateScheduleSerializer(data=data)
        if ser.is_valid(raise_exception=False):
            ser.save()
            return send_200(
                data={"data": ser.data}, message="schedule created/updated successfully"
            )
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )
