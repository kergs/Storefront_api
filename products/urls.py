from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]

category_urlpatterns = [
    path('', views.CategoryListCreateView.as_view(), name='category-list'),
]