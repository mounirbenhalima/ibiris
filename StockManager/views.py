from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory, forms
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import date
from datetime import datetime
from django.urls import reverse_lazy, resolve
from django.core.mail import send_mail, EmailMessage
from django.db import IntegrityError
from django.utils.crypto import get_random_string
import io
from django.db.models import Q
from django.http import FileResponse
from reportlab.pdfgen import canvas
from decimal import Decimal
from .utils import render_to_pdf

from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)

from Product.models import Batch, Product
from Company.models import Company
from .models import Purchase, Consumption
from django.template import loader, Context

class ProductIndexView(View):
    template_name = 'stock_manager/index_product.html'

    def get(self, request):
        return render(request, "stock_manager/index_product.html")

class IndexView(View):
    template_name = 'stock_manager/index.html'

    def get(self, request):
        return render(request, "stock_manager/index.html")

class PurchaseCreateView(View):
    model = Purchase
    template_name = 'stock_manager/purchase.html'
    success_url = reverse_lazy('stock-manager:purchase-list')

    def get(self, request, *arg, **kwargs):
        context = {
            'products': Product.objects.all(),
        }
        return render(self.request, 'stock_manager/purchase.html', context)

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            product = None
            product_slug = request.POST.get('product')
            batch_ref = request.POST.get('batch')
            quantity = int(request.POST.get('qte'))
            exp_date = request.POST.get('exp_date')
            try:
                product = Product.objects.get(slug = product_slug)
            except:
                product = None

            if product != None:
                try:
                    batch = Batch.objects.get(ref = batch_ref)
                except:
                    batch = None
                    
                if batch is None:
                    batch = Batch(product=product, ref = batch_ref, quantity = quantity, order_date = timezone.now(), expiring_date = exp_date )
                    batch.save()
                else:
                    if batch.product != product:
                        messages.error(request, "Conflit LOT/PRODUIT !")
                        return redirect(request.META.get('HTTP_REFERER'))
                    batch.quantity += quantity
                    batch.save()
                ref=get_random_string(15)
                purchase = Purchase(order_date=timezone.now(), user=request.user, batch = batch, quantity=quantity, ref_code = ref)
                purchase.save()

                product.quantity += quantity
                product.save()
                                
            else:
                messages.error(request, "Erreur !")
                return redirect(request.META.get('HTTP_REFERER'))
            return redirect(self.success_url)


class ConsumptionCreateView(View):
    model = Consumption
    template_name = 'stock_manager/consumption.html'
    success_url = reverse_lazy('stock-manager:consumption-list')

    def get(self, request, *arg, **kwargs):
        return render(self.request, 'stock_manager/consumption.html')

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            batch_ref = request.POST.get('batch')
            quantity = int(request.POST.get('qte'))
            try:
                batch = Batch.objects.get(slug = batch_ref)
            except:
                batch = None
                    
            if batch is None:
                messages.error(request, "Lot Inexistant !")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                if quantity > batch.quantity:
                    messages.error(request, "Veuillez Vérifier la Quantité !")
                    return redirect(request.META.get('HTTP_REFERER'))
                batch.quantity -= quantity
                batch.save()
            ref=get_random_string(15)
            consumption = Consumption(order_date=timezone.now(), user=request.user, batch = batch, quantity=quantity, ref_code = ref)
            consumption.save()

            batch.product.quantity -= quantity
            batch.product.save()
                                
        else:
            messages.error(request, "Erreur !")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(self.success_url)


class PurchaseList(ListView):
    queryset = Purchase.objects.all()
    template_name = 'stock_manager/list/purchase_list.html'
    paginate_by = 20

class ConsumptionList(ListView):
    queryset = Consumption.objects.all()
    template_name = 'stock_manager/list/consumption_list.html'
    paginate_by = 20




def stock_status(request):
    products = Product.objects.all()
    batches = Batch.objects.exclude(quantity = 0).all()
    try:
        company = Company.objects.get(name='')
    except:
        company = ''
    template = loader.get_template('invoices/stock_status.html')
    context = {
        "user": request.user,
        "company": company,
        "products": products,
        "batches": batches,
    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/stock_status.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (timezone.now())
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")