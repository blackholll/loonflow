from django.urls import path
from apps.account.views import UserView, UserDetailView, RoleView, DeptView, UserRoleView, RoleUserView, \
    UserResetPasswordView, RoleDetailView, \
    DeptDetailView, SimpleUserView, UserChangePasswordView, \
    DeptTreeView, SimpleDeptTreeView, UserProfileView, SimpleRoleView, ApplicationView, SimpleApplicationView, \
    ApplicationDetailView, ApplicationWorkflowView, TenantDetailView

urlpatterns = [
    path('/users', UserView.as_view()),
    path('/my_profile', UserProfileView.as_view()),
    path('/simple_users', SimpleUserView.as_view()),
    path('/users/change_password', UserChangePasswordView.as_view()),
    path('/users/<int:user_id>', UserDetailView.as_view()),
    path('/users/<int:user_id>/roles', UserRoleView.as_view()),
    path('/users/<int:user_id>/reset_password', UserResetPasswordView.as_view()),
    path('/roles', RoleView.as_view()),
    path('/roles/<int:role_id>', RoleDetailView.as_view()),
    path('/simple_roles', SimpleRoleView.as_view()),
    path('/roles/<int:role_id>/users', RoleUserView.as_view()),
    path('/depts_tree', DeptTreeView.as_view()),
    path('/depts', DeptView.as_view()),
    path('/simple_depts_tree', SimpleDeptTreeView.as_view()),
    path('/depts/<int:dept_id>', DeptDetailView.as_view()),
    path('/applications', ApplicationView.as_view()),
    path('/applications/<str:application_id>', ApplicationDetailView.as_view()),
    path('/applications/<int:application_id>/workflows', ApplicationWorkflowView.as_view()),
    path('/simple_applications', SimpleApplicationView.as_view()),
    path('/tenants/<str:tenant_id>', TenantDetailView.as_view()),



]
