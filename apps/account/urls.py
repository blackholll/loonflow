from django.urls import path
from apps.account.views import UserView, UserDetailView, RoleView, DeptView, AppTokenView, \
    AppTokenDetailView, UserRoleView, RoleUserView, UserResetPasswordView, RoleDetailView, \
    DeptDetailView, \
    RoleUserDetailView, SimpleUserView, SimpleAppTokenView, SimpleDeptView, UserChangePasswordView, \
    TenantView, DeptTreeView, SimpleDeptTreeView, UserProfileView

urlpatterns = [
    path('/users', UserView.as_view()),
    path('/my_profile', UserProfileView.as_view()),
    path('/simple_users', SimpleUserView.as_view()),  # exception optimize done
    # path('/users/change_password', UserChangePasswordView.as_view()),
    # path('/simple_users', SimpleUserView.as_view()),
    path('/users/<int:user_id>', UserDetailView.as_view()),  # exception optimize done
    # path('/users/<int:user_id>/roles', UserRoleView.as_view()),
    # path('/users/<int:user_id>/reset_password', UserResetPasswordView.as_view()),
    # path('/roles', RoleView.as_view()),
    # path('/roles/<int:role_id>', RoleDetailView.as_view()),
    # path('/roles/<int:role_id>/users', RoleUserView.as_view()),
    # path('/roles/<int:role_id>/users/<int:user_id>', RoleUserDetailView.as_view()),

    path('/depts_tree', DeptTreeView.as_view()),
    path('/depts', DeptView.as_view()),
    path('/simple_depts_tree', SimpleDeptTreeView.as_view()),
    path('/depts/<int:dept_id>', DeptDetailView.as_view()),
    # path('/app_token', AppTokenView.as_view()),
    # path('/simple_app_token', SimpleAppTokenView.as_view()),
    # path('/app_token/<int:app_token_id>', AppTokenDetailView.as_view()),
    # path('/tenants', TenantView.as_view())
]
