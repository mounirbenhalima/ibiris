from django.contrib import admin

from Product.models import (
    Brand,
    Color,
    Product,
    Range,

)

from django.forms import CheckboxSelectMultiple
from django.db import models

admin.site.register(Range)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Product)