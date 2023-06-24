from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('store/', views.store_view, name='base_store'),
    path('store/f~<str:query>/', views.filtered_store_view, name='filtered_store'),
    path('store/<slug:slug>/', views.product_view, name='product_detail'),
]