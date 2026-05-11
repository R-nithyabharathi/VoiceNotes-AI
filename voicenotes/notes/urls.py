from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('save/', views.save_note, name="save_note"),
    path('download/', views.download_notes),
    path('delete/<int:id>/', views.delete_note),
    path('video/', views.video_to_text),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
]