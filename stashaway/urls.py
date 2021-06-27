from django.urls import path
from stashaway.api import SchemeInfo, PortfolioInfo, RecurringScheduleInfo, DepositInfo

urlpatterns = [
    path(r"schemes/", SchemeInfo.as_view(), name="get or create schemes"),
    path(f"portfolios/", PortfolioInfo.as_view(), name="get or create portfolios"),
    path(
        f"monthly-schedule/",
        RecurringScheduleInfo.as_view(),
        name="create a montly schedule for deposits",
    ),
    path(
        r"deposits/",
        DepositInfo.as_view(),
        name="get or create deposits into portfolios",
    ),
]
