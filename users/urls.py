from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user, no_permission, group_list, assign_role, create_group
from events.views import participants_list

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='sign_out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('participants/', participants_list, name='participants_list'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create_group'),
    path('admin/group-list/', group_list, name='group_list'),
    path('no-permission/', no_permission, name='no-permission'),
]
