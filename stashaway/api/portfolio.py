from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Subquery, OuterRef, Sum, Q
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from code_service.libs.response import send_200, send_400
from code_service.validators import csv_uuid_validator, uuid_validator
from user.validators import user_id_validator
from stashaway.models import Portfolio, Deposit


class GetPortfolioSerializer(Serializer):
    user = serializers.CharField(validators=(uuid_validator, user_id_validator,))
    scheme_ids = serializers.CharField(
        allow_null=True, default=None, validators=(csv_uuid_validator,)
    )

    def to_representation(self, data):
        if data["scheme_ids"] is None:
            portfolios = Portfolio.objects.filter(user=data["user"])
        else:
            portfolios = Portfolio.objects.filter(
                user=data["user"], scheme_id__in=data["scheme_ids"]
            )
        portfolios = portfolios.annotate(
            deposit_amount=Subquery(
                Deposit.objects.filter(portfolio_id=OuterRef("id"))
                .values("portfolio_id")
                .annotate(amount_total=Sum("amount"))
                .values("amount_total")[:1]
            )
        )
        return {
            "data": [
                {
                    "scheme_id": p.scheme_id,
                    "id": p.id,
                    "deposit_amount": p.deposit_amount,
                }
                for p in portfolios
            ]
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class CreatePortfolioSerializer(Serializer):
    user = serializers.CharField(validators=(uuid_validator, user_id_validator,))
    scheme_id = serializers.CharField(validators=(uuid_validator,))

    def validate(self, data):
        old_portfolio = Portfolio.objects.filter(
            user=data["user"], scheme_id=data["scheme_id"]
        ).first()
        if old_portfolio is not None:
            raise serializers.ValidationError(
                "Portfolio for this scheme already exists for the user"
            )
        return data

    def create(self, data):
        return Portfolio.objects.create(
            user_id=data["user"], scheme_id=data["scheme_id"]
        )

    def to_representation(self, portfolio: Portfolio):
        return {
            "id": portfolio.id,
        }

    def extract_error_msg(self):
        errors = self.errors
        for key, msg in errors.items():
            return str(msg[0])
        return "Error in fetching results"


class PortfolioInfo(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="user id",
            ),
            openapi.Parameter(
                "scheme_ids",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description="comma seperated scheme IDs",
            ),
        ]
    )
    def get(self, request):
        """
        Get protflios of an user
        """
        q_data = request.query_params
        ser = GetPortfolioSerializer(data=q_data)
        if ser.is_valid(raise_exception=False):
            return send_200(data=ser.data, message="portfolios retrieved successfully")
        return send_400(
            status="FAILED",
            data={"errors": ser.errors},
            message=ser.extract_error_msg(),
        )

    @swagger_auto_schema(request_body=CreatePortfolioSerializer)
    def post(self, request):
        """
        Register a new portfolio for user
        """
        data = dict(request.data)
        ser = CreatePortfolioSerializer(data=data)
        if ser.is_valid(raise_exception=False):
            ser.save()
            return send_200(
                data={"data": ser.data}, message="portfolio created successfully"
            )
        else:
            return send_400(
                status="FAILURE",
                data={"errors": ser.errors},
                message=ser.extract_error_msg(),
            )
