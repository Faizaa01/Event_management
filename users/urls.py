from users.views import sign_up,sign_out,activate_user, no_permission, group_list, assign_role, create_group, CustomLoginView, ProfileView, EditProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from events.views import participants_list
from django.urls import path
from users.views import run_migrations


urlpatterns = [
    path('run-migrations/', run_migrations),

    path('sign_up/', sign_up, name='sign_up'),
    # path('sign_in/', sign_in, name='sign_in'),
    path('sign_in/', CustomLoginView.as_view(), name='sign_in'),
    path('sign_out/', sign_out, name='sign_out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),

    path('participants/', participants_list, name='participants_list'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create_group'),
    path('admin/group-list/', group_list, name='group_list'),
    path('no-permission/', no_permission, name='no-permission'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
