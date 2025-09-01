from django.contrib import admin
from django.urls import path
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),  
    path('ticket_booking/', views.ticket_booking, name='ticket_booking'),
    path('search_tickets/', views.search_tickets, name='search_tickets'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.UserProfile, name='UserProfile'),  
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('download_ticket/<str:pnr>/', views.download_ticket_pdf, name='download_ticket_pdf'),
]
