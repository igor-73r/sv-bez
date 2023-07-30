from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('store/', views.base_store_view, name='base_store'),
    path('store/category=<int:category>', views.base_store_view, name='cat_store'),
    path('store/<slug:slug>/', views.product_view, name='product_detail'),
]
