from django.urls import path, include
from .views import (
    IndexView,
    PurchaseList,
    ConsumptionList,
    PurchaseCreateView,
    ConsumptionCreateView,
    stock_status,
    ProductIndexView,
)

app_name = 'stock-manager'


urlpatterns = [

    path('stock-manager-product/', ProductIndexView.as_view(), name='index-product'),
    

    # ## ##
    path('', IndexView.as_view(), name='index'),
    path('purchase/', PurchaseCreateView.as_view(), name="purchase"),
    path('consumption/', ConsumptionCreateView.as_view(), name="consumption"),
    path('purchase-list/', PurchaseList.as_view(), name="purchase-list"),
    path('consumption-list/', ConsumptionList.as_view(), name="consumption-list"),

    path('inventory/', stock_status, name="stock-status"),
]
