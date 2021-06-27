from django.db import models
from django.db.models.deletion import CASCADE

from code_service.core.abstract_models import BigIDAbstract
from code_service.constants import SchemeTypes, DepositTypes

# Create your models here.


class Scheme(BigIDAbstract):
    name = models.CharField(max_length=1000)
    scheme_type = models.CharField(
        choices=[(t.value, t.value) for t in SchemeTypes], max_length=100
    )


class Portfolio(BigIDAbstract):
    user = models.ForeignKey("user.UserProfile", on_delete=CASCADE)
    scheme = models.ForeignKey("Scheme", on_delete=CASCADE)


class MonthlyRecurringDepositSchedule(BigIDAbstract):
    portfolio = models.ForeignKey("Portfolio", on_delete=CASCADE, unique=True)
    day_of_month = models.IntegerField()


class Deposit(BigIDAbstract):
    portfolio = models.ForeignKey("Portfolio", on_delete=CASCADE)
    amount = models.PositiveBigIntegerField()
    deposit_type = models.CharField(
        choices=[(t.value, t.value) for t in DepositTypes], max_length=100
    )
