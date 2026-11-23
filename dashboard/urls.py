from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    # Sản phẩm
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    # Đơn hàng + SMTP
    path('orders/', views.order_list, name='order_list'),
    path('orders/update/<int:pk>/', views.order_update_status, name='order_update_status'),
    # Khách hàng, Báo cáo, Cài đặt
    path('customers/', views.customer_list, name='customer_list'),
    path('reports/', views.report_view, name='report_view'),
    path('reports/export-csv/', views.export_orders_csv, name='export_orders_csv'),
    path('settings/', views.settings_view, name='settings_view'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/update/<int:pk>/', views.order_update_status, name='order_update_status'),
    path('customers/', views.customer_list, name='customer_list'),
    path('reports/', views.report_view, name='report_view'),
    path('reports/export-csv/', views.export_orders_csv, name='export_orders_csv'),
    path('settings/', views.settings_view, name='settings_view'),
]