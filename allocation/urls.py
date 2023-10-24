from django.urls import path
from . import views
urlpatterns=[
    path("",views.login),
    path("register",views.register),
    path("logins",views.logins),
    path("logout",views.login),
    path("staffselection",views.staffselection),
    path("edition",views.edition),
    path('edit/',views.edit),
    path('rooms/',views.roomss),
    path('roomselect',views.roomselect),
    path('examdate',views.examdate), 
    path('staffedition/',views.staffed), 
    path('addition',views.addition), 
    path('deletion',views.deletion), 
    path('endsems',views.end1),
    path('endsem',views.endsem1),
    path('edstaff',views.edstaff),
    path('download-multiple/', views.download_multiple_files, name='download_multiple_files'),
]