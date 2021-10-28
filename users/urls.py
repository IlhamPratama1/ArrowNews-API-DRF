from django.urls import path

from .views import (BlacklistTokenUpdateView, CustomUserCreate, MyProfileView,
                    UserProfile, EditMyProfile)

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', UserProfile.as_view(), name="user_profile"),
    path('myprofile/', MyProfileView.as_view(), name="my_profile"),
    path('myprofile/edit/', EditMyProfile.as_view(), name="edit_my_profile"),
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
