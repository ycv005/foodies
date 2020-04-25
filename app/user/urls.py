from django.urls import path
from user.views import UserCreateView, CreateTokenView, ModifyUserView

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('update/', ModifyUserView.as_view(), name='update')
]
