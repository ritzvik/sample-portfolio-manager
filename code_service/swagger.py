import base64
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


swagger_schema_view = get_schema_view(
    openapi.Info(title="API Docs for code-service", default_version="v1",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
