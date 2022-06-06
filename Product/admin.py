from django.contrib import admin

from Product.models import (
    Brand,
    Product,
    Range,
    Batch,

)

from django.forms import CheckboxSelectMultiple
from django.db import models

admin.site.register(Range)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Batch)