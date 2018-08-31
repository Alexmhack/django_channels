from django.urls import path

from .views import (
	user_list,
)

app_name = 'display'

urlpatterns = [
	path('', user_list, name='user-list'),
]
