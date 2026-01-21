from django.urls import path
from . import views

urlpatterns = [
    path('', views.lecture_list, name='lecture_list'),
    path('lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    path('lecture/<int:lecture_id>/review/', views.review_create, name='review_create'),
    path('review/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path("signup/", views.signup, name="signup"),
    path("lecture/<int:lecture_id>/like/", views.lecture_like, name="lecture_like"),
    path("review/<int:review_id>/like/", views.review_like, name="review_like"),

]
