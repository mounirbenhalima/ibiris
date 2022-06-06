from django.urls import path, include
from .views import *

app_name = 'product'

urlpatterns = [
     # Main View
     path('', ProductIndexView.as_view(), name='index'),
     # Brands Url Management
     path('brand/list/', BrandListView.as_view(), name='brands'),
     path('brand/create/', BrandCreateView.as_view(), name='brand-create'),
     path('brand/<slug>/update/', BrandUpdateView.as_view(), name='brand-update'),
     path('brand/<slug>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

     # Ranges Url Management
     path('product/range/list/', RangeListView.as_view(), name='ranges'),
     path('product/range/create/', RangeCreateView.as_view(), name='range-create'),
     path('product/range/<slug>/update/', RangeUpdateView.as_view(), name='range-update'),
     path('product/range/<slug>/delete/',RangeDeleteView.as_view(), name='range-delete'),


     # Flavors Url Management
     path('flavor/list/', FlavorListView.as_view(), name='flavors'),
     path('flavor/create/', FlavorCreateView.as_view(), name='flavor-create'),
     path('flavor/<slug>/update/', FlavorUpdateView.as_view(), name='flavor-update'),
     path('flavor/<slug>/delete/', FlavorDeleteView.as_view(), name='flavor-delete'),

     # # Product List Url
     path('product/list/product/',ProductListView.as_view(), name='products'),
     path('product/list/batch/',batch_list, name='batches'),

     # # Product Creation Url
     path('product/create/product/',ProductCreateView.as_view(), name='product-create'),

     # # Product Update Url
     path('product/product/<slug>/update/',ProductUpdateView.as_view(), name='product-update'),

     # # Product Delete Url
     path('product/<slug>/delete/',ProductDeleteView.as_view(), name='product-delete'),

     path('print-batch-code/<slug>/', print_batch_code, name='print-batch-code'),

]
