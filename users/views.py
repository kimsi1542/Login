from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer


# 회원가입 View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인 View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "로그인 정보가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    # 사용자 로그아웃 API POST 요청을 받으면 사용자의 인증 토큰을 삭제합니다.

    # 로그인한 사용자만 접근 가능하도록 설정
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 요청을 보낸 사용자의 토큰을 삭제
            request.user.auth_token.delete()
            return Response(
                {"message": "성공적으로 로그아웃 되었습니다."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "로그아웃 처리 중 문제가 발생했습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

#비밀번호 변경 View
class ChangePasswordView(APIView):

    # 로그인한 사용자만 접근 가능하도록 설정
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            # 1. 기존 비밀번호가 맞는지 확인
            if not user.check_password(old_password):
                return Response(
                    {"error": "기존 비밀번호가 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. 새 비밀번호 설정 및 저장 (자동으로 해싱됨)
            user.set_password(new_password)
            user.save()

            # 3. 보안을 위해 기존 토큰 파기 (강제 로그아웃 효과)
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()

            return Response(
                {"message": "비밀번호가 성공적으로 변경되었습니다. 새로운 비밀번호로 다시 로그인해주세요."},
                status=status.HTTP_200_OK
            )

        # 입력값이 누락되었을 경우 에러 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#계정삭제 View
class DeleteAccountView(APIView):
    """
    회원 탈퇴 API
    DELETE 요청을 받아 현재 로그인된(토큰을 보낸) 사용자의 계정을 영구적으로 삭제합니다.
    """
    permission_classes = [IsAuthenticated]  # 로그인한 유저만 탈퇴 가능

    def delete(self, request):
        user = request.user

        try:
            # 유저 삭제 (DB에서 영구 삭제 및 연관된 CASCADE 데이터 자동 삭제)
            user.delete()

            return Response(
                {"message": "회원 탈퇴가 완료되었습니다. 그동안 이용해 주셔서 감사합니다."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "회원 탈퇴 처리 중 문제가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )