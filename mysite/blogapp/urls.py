from django.urls import path

from .views import *

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticlesListView.as_view(), name="articles"),
]
