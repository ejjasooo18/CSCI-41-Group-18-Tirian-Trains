from django.urls import path
from . import views

# from .views import (ThreadListView,
#                     ThreadDetailView,
#                     ThreadCreateView,
#                     ThreadUpdateView)

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('buy/<int:trip_id>/', views.buy_ticket, name='buy_ticket'),
]

app_name = 'main'