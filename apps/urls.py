from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.views import CategoryListView, CustomLoginView, ProductListView, ProductDetailView, \
    WishListView, LikeProductView, OrderListView, MarketListView

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('product/list', ProductListView.as_view(), name='product_list'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('wishlist', WishListView.as_view(), name='wishlist'),
    path('product/liked/<str:slug>', LikeProductView.as_view(), name='liked'),
    path('product/order-list', OrderListView.as_view(), name='order-list'),
]

urlpatterns += [
    path('admin_page/market', MarketListView.as_view(), name='market'),
]

