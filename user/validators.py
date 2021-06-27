from user.models import UserProfile
from rest_framework import serializers


def user_id_validator(user_id: str) -> UserProfile:
    user = UserProfile.objects.filter(id=user_id).first()
    if user:
        return user
    else:
        raise serializers.ValidationError("user not found")
