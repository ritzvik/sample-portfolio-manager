from django.urls import path
from user.api.user import UserInfo

urlpatterns = [
    path(r"", UserInfo.as_view(), name="get or create users"),
]
