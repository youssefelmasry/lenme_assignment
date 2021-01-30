from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
        email=validated_data['email'],
        password=validated_data['password'],
        username=validated_data['username'],
        usertype=validated_data['usertype']
    )
        user.save()
        
        return user

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username','usertype', 'token']
        extra_kwargs = {'email': {'required': True},
                        'password': {'write_only': True},
                        'email': {'write_only': True},
                        'username': {'write_only': True}}

class CustomObtainTokenSerializer(TokenObtainPairSerializer):

    """Custom Token Obtain to validate with username and email instead of username only"""

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = get_user_model().objects.filter(email=attrs.get("username")).first() or get_user_model().objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)