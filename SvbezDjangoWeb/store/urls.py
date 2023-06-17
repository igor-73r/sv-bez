from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('store/', views.store_view, name='base_store'),
    path('store/<str:pk>', views.product_view, name='product_detail')
]