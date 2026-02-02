from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    # The Home Dashboard
    path('dashboard/', views.home, name='home'),
    
    # Buy Ticket / Schedule page
    path('schedule/', views.trip_list, name='trip_list'),
    
    # Booking page
    path('buy/<int:trip_id>/', views.buy_ticket, name='buy_ticket'),
    
    # View My Trips page
    path('my-trips/', views.my_trips, name='my_trips'),
    
    # Redirect the root URL to the login page
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    
    # User Registration
    path('register/', views.register, name='register'),
]

app_name = 'main'