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
    path('rooms/',views.rooms),
    path('rooms/',views.rooms),
    path('roomselect',views.roomselect),
    path('examdate',views.examdate), 
    path('download/', views.download_file, name='download_file'),
    path('download-multiple/', views.download_multiple_files, name='download_multiple_files'),
]