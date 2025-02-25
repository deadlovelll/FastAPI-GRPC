from rest_framework import serializers

class TokenValidationSuccessSerializer(serializers.Serializer):
    valid = serializers.BooleanField(help_text="Indicates if the token is valid")
    payload = serializers.CharField(help_text="The decoded payload of the token")


class TokenValidationErrorSerializer(serializers.Serializer):
    IS_VALID = serializers.BooleanField(help_text="Indicates if the token is valid")
    DETAIL = serializers.CharField(help_text="Error details")
