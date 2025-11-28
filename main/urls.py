from django.urls import path
from . import views

# from .views import (ThreadListView,
#                     ThreadDetailView,
#                     ThreadCreateView,
#                     ThreadUpdateView)

urlpatterns = [
    # The Home Dashboard
    path('dashboard/', views.home, name='home'),
    
    # Buy Ticket / Schedule page
    path('schedule/', views.trip_list, name='trip_list'),
    
    # Booking page
    path('buy/<int:trip_id>/', views.buy_ticket, name='buy_ticket'),
    
    # View My Trips page
    path('my-trips/', views.my_trips, name='my_trips'),
]

app_name = 'main'