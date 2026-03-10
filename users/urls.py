from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, DeleteAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    #로그아웃 추가
    path('logout/', LogoutView.as_view(), name='logout'),
    #비밀번호 바꾸기
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    #계정 삭제
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]