from django.urls import path
from apps.account.views import LoonUserView, LoonRoleView, LoonDeptView, LoonAppTokenView, LoonAppTokenDetailView

urlpatterns = [
    path('/users', LoonUserView.as_view()),
    path('/roles', LoonRoleView.as_view()),
    path('/depts', LoonDeptView.as_view()),
    path('/app_token', LoonAppTokenView.as_view()),
    path('/app_token/<int:app_token_id>', LoonAppTokenDetailView.as_view()),
]
