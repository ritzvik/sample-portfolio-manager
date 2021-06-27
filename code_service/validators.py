from uuid import UUID
from typing import List
from rest_framework import serializers


def uuid_validator(string: str) -> str:
    try:
        UUID(string)
        return string
    except:
        raise serializers.ValidationError("Not a valid UUID")


def list_uuid_validator(string_list: List[str]) -> List[str]:
    for s in string_list:
        uuid_validator(s)


def csv_uuid_validator(csv_uuids: str) -> List[str]:
    uuid_list = list(csv_uuids.strip().split(","))
    list_uuid_validator(uuid_list)
    return uuid_list
