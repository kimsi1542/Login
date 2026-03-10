from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 비밀번호 해싱을 위해 create_user 사용
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    # 비밀번호 변경을 위한 시리얼라이저

    old_password = serializers.CharField(required=True, write_only=True, help_text="기존 비밀번호")
    new_password = serializers.CharField(required=True, write_only=True, help_text="새 비밀번호")