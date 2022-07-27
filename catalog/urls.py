from django.urls import path
from catalog.views import *


urlpatterns = [
    path('accounts/settings/', account_settings, name='account_settings'),
    path('products/<slug:category_slug>/', show_all_products_category, name='products'),
    path('dungeon/', category_dungeon, name='category'),
    path('order-added/', order_successful_add, name='order-added'),
    path('orders-max-reached/', order_max_reached, name='orders-max-reached'),
    path('requested-orders/<int:order_id>/', requested_order_for_drivers, name='requested-order'),
    path('requested-orders-pending/', requested_order_status_pending, name='requested-orders-pending'),
    path('requested-orders-paid/', requested_order_status_paid, name='requested-orders-paid'),
    path('requested-orders-processing/', requested_order_status_processing, name='requested-orders-processing'),
    path('requested-orders-complete/', requested_order_status_complete, name='requested-orders-complete'),
    path('requested-orders/', requested_orders_for_drivers, name='requested-orders'),
    path('customer-orders/<int:order_id>/', CustomerOrder, name='customer-order'),
    path('customer-orders-filter/', CustomerOrdersFilter, name='customer-orders-filter'),
    path('customer-orders/', CustomerOrders, name='customer-orders'),
    path('delet-bided-order//<int:order_id>/', DeletBidedOrder, name='delet-bided-order'),
    path('bid-order/<int:order_id>/<str:order_total>/', bid_order,  name='bid_order'),
    path('deleted-bid-message/', deleted_bid_message,  name='deleted-bid-message'),
    path('<slug:game_slug>/<slug:category_slug>/<slug:product_slug>/', show_product_by_category,
         name='product_by_category'),
    path('', index, name='index'),
]