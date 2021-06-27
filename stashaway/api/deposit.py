from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.constants.stashaway_constants import DepositTypes
from code_service.libs.response import send_200, send_400
from code_service.utils.datetime_utils import get_present_datetime_in_utc
from stashaway.models import Portfolio, MonthlyRecurringDepositSchedule, Deposit
from code_service.validators import uuid_validator


class GetDepositDetailsSerializer(Serializer):
    portfolio_id = serializers.CharField(validators=(uuid_validator,))

    def validate(self, data):
        portfolio = Portfolio.objects.filter(id=data["portfolio_id"]).first()
        if portfolio is None:
            raise serializers.ValidationError("portfolio not found")
        return data

    def to_representation(self, data):
        deposits = Deposit.objects.filter(portfolio_id=data["portfolio_id"]).order_by(
            "-created_on"
        )
        return {
            "data": [
                {"deposit_date": d.created_on, "amount": d.amount} for d in deposits
            ]
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class CreateDepositSerializer(Serializer):
    portfolio_id = serializers.CharField(validators=(uuid_validator,))
    amount = serializers.IntegerField(min_value=0)
    deposit_type = serializers.ChoiceField(choices=[t.value for t in DepositTypes])

    def validate(self, data):
        portfolio = Portfolio.objects.filter(id=data["portfolio_id"]).first()
        if portfolio is None:
            raise serializers.ValidationError("portfolio not found")

        if data["deposit_type"] == DepositTypes.RECURRING.value:
            old_monthly_deposit = (
                Deposit.objects.filter(
                    portfolio_id=data["portfolio_id"], deposit_type=data["deposit_type"]
                )
                .order_by("-created_on")
                .first()
            )
            deposit_obj = MonthlyRecurringDepositSchedule.objects.filter(
                portfolio_id=data["portfolio_id"]
            ).first()
            if deposit_obj is None:
                raise serializers.ValidationError("no monthly deposit schedule found")
            if old_monthly_deposit is not None:
                now = get_present_datetime_in_utc()
                if old_monthly_deposit.created_on.month == now.month:
                    raise serializers.ValidationError("already deposited for the month")
        return data

    def create(self, data):
        return Deposit.objects.create(
            portfolio_id=data["portfolio_id"],
            amount=data["amount"],
            deposit_type=data["deposit_type"],
        )

    def to_representation(self, deposit: Deposit):
        return {
            "portfolio_id": deposit.portfolio_id,
            "amount": deposit.amount,
            "deposit_type": deposit.deposit_type,
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class DepositInfo(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "portfolio_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def get(self, request):
        """
        Get all deposits in a portfolio
        """
        ser = GetDepositDetailsSerializer(data=request.query_params)
        if ser.is_valid(raise_exception=False):
            return send_200(data=ser.data, message="deposit details fetched")
        return send_400(
            status="FAILURE",
            data={"errors": ser.errors},
            message=ser.extract_error_msg(),
        )

    @swagger_auto_schema(request_body=CreateDepositSerializer)
    def post(self, request):
        """
        Deposit to a portfolio
        """
        data = dict(request.data)
        ser = CreateDepositSerializer(data=data)
        if ser.is_valid(raise_exception=False):
            ser.save()
            return send_200(
                data={"data": ser.data}, message="deposit created successfully"
            )
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )
