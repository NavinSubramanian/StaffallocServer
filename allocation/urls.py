from django.urls import path
from . import views
urlpatterns=[
    path("",views.home),
    path("register",views.register), # Register Function of form
    path("logins",views.logins), # Login Page
    path("logout",views.logout_user), # Logout Function
    path("staffselection",views.staffselection),
    path("edition",views.edition),
    path('edit/',views.edit),
    path('rooms/',views.roomss),
    path('roomselect',views.roomselect),
    path('examdate',views.examdate), 
    path('staffedition/',views.staffed),  # Add/Del Staff Page
    path('addition',views.addition), 
    path('deletion',views.deletion), 
    path('endsems',views.end1),
    path('endsem',views.endsem1),
    path('edstaff',views.edstaff),
    path('download-multiple/', views.download_multiple_files, name='download_multiple_files'),
    path('dashboard',views.admins)  # Staff Selection Page
]