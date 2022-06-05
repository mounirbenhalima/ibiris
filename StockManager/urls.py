from django.urls import path, include
from .views import (
    product_entry,
    product_out,
    IndexView,
    add_to_cart,
    OrderSummaryView,
    validate_order,
    delete_order,
    EntryStockList,
    remove_from_cart,
    email,
    stock_movement,
    OrderList,
    OrderDetail,
    stock_status,
    RecapPage,
    recap,
    ProductIndexView,
)

app_name = 'stock-manager'


urlpatterns = [

    path('stock-manager-product/', ProductIndexView.as_view(), name='index-product'),
    
    # Raw Matter
    path('stock-entry/product/', product_entry, name="product-entry"),
    path('stock-out/product/', product_out, name="product-out"),
    path('stock-return/product/', product_entry, name="product-return"),
    path('stock-status/product/', product_entry, name="product-status"),

    # ## ##
    path('', IndexView.as_view(), name='index'),
    path('add-to-order/<slug>/', add_to_cart, name="add-to-order"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('order-validation/', validate_order, name="order-validation"),
    path('order-delete/<slug>/', delete_order, name="order-delete"),
    path('orders-entry/', EntryStockList.as_view(), name="orders-entry"),
    path('remove-item/<identifier>/', remove_from_cart, name="remove-item"),
    path('orders-list/', OrderList.as_view(), name="orders-list"),
    path('stock-invoice/<slug>/', stock_movement, name="invoice"),
    path('order-detail/<slug>/', OrderDetail.as_view(), name="order-detail"),

    path('inventory/', stock_status, name="stock-status"),

    path('recap-page/', RecapPage.as_view(), name='recap-page'),
    path(r'^recap/search/', recap, name='recap'),
    # Mail TEst
    path('send-mail/', email),
]
