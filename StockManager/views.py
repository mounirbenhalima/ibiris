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
from .forms import ContactChoiceForm
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

from Product.models import Product, Color
from Company.models import Company
from .models import Order, OrderItem
from django.template import loader, Context

class ProductIndexView(View):
    template_name = 'stock_manager/index_product.html'

    def get(self, request):
        return render(request, "stock_manager/index_product.html")

class IndexView(View):
    template_name = 'stock_manager/index.html'

    def get(self, request):
        return render(request, "stock_manager/index.html")

# ----------------RAW MATTER-----------------


@login_required(login_url=reverse_lazy('login'))
def product_entry(request):
    context = {
        'product_list': Product.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Achat "
    }
    try:
        active_order = Order.objects.get(ordered=False)
    except:
        active_order = None
    if active_order:
        if active_order.type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


@login_required(login_url=reverse_lazy('login'))
def product_out(request):
    context = {
    'product_list': Product.objects.all(),
    "STOCK_TYPE": "STOCK_OUT",
    "form_name": "Vente"
    }
    try:
        active_order = Order.objects.get(ordered=False)
    except:
        active_order = None
    if active_order:
        if active_order.type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


@login_required(login_url=reverse_lazy('login'))
def product_return(request):
    context = {
        'product_list': Product.objects.all(),
        "STOCK_TYPE": "STOCK_RETURN",
        "form_name": "Retour"
    }
    active_order = Order.objects.get(ordered=False)
    if active_order:
        if active_order.type_order == 'STOCK_RETURN':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

###################################################################


def add_to_cart(request, slug):
    try:
        order = Order.objects.get(ordered=False)
    except:
        order = None
    item = get_object_or_404(Product, slug=slug)
    if order is not None:
        for i in order.items.all():
            if i.item.slug == item.slug:
                order.items.remove(i)
                orderitem = OrderItem.objects.get(identifier=i.identifier)
                orderitem.delete()
        identifier = get_random_string(10)
        order_item = OrderItem(
        item=item,
        user=request.user,
        ordered=False,
        identifier = identifier
        )
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Veuillez Remplir La Quantité")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
                order.save()
                order.items.add(order_item)
                order.save()
    else:
        identifier = get_random_string(10)
        order_item = OrderItem(
        item=item,
        user=request.user,
        ordered=False,
        identifier = identifier
        )
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Veuillez Remplir La Quantité")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
                order = Order(
                    ordered_date = timezone.now(),
                    user = request.user,
                    type_order = STOCK_TYPE
                )
                order.save()
                order.items.add(order_item)
                order.save()
    if STOCK_TYPE == "STOCK_ENTRY":
        order_item.price = order_item.item.cost
        order_item.save()
        return redirect("stock-manager:product-entry")
    elif STOCK_TYPE == "STOCK_OUT":
        order_item.price = order_item.item.price
        order_item.save()
        return redirect("stock-manager:product-out")
    elif STOCK_TYPE == "STOCK_RETURN":
        return redirect("stock-manager:product-return")


class EntryStockList(ListView):
    template_name = 'stock_manager/list/entry_orders.html'
    queryset = Order.objects.filter(ordered=True)


class OrderSummaryView(LoginRequiredMixin, View):
    template_name = 'stock_manager/list/order_summary.html'
    form = ContactChoiceForm()

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(ordered=False)
        except ObjectDoesNotExist:
                messages.error(
                    self.request, "Vous N'Avez Aucune Commande Active".upper())
                return redirect(self.request.META.get('HTTP_REFERER'))
        context = {
            'object': order,
            'form': self.form,
        }
        return render(self.request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = ContactChoiceForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            order = Order.objects.get(ordered=False)
            order.supplier = form.supplier
            order.save()
            return redirect('stock-manager:order-summary')

def delete_order(request, slug):
    order = get_object_or_404(Order, slug = slug)
    if order.type_order == "STOCK_OUT":
        for item in order.items.all():
            item.item.quantity += item.quantity
            item.item.save()
    elif order.type_order == "STOCK_ENTRY" or order.type_order == "STOCK_RETURN":
        for item in order.items.all():
            item.item.quantity -= item.quantity
            item.item.save()
        
    order.delete()

    return redirect(reverse_lazy("stock-manager:order-consulting"))


def validate_order(request):
    try:
        order = Order.objects.get(ordered=False)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('stock-manager:index'))

    if order.type_order == "STOCK_ENTRY" or order.type_order == "STOCK_RETURN":
        for order_item in order.items.all():
            item = get_object_or_404(Product, slug=order_item.item.slug)
            item.quantity += order_item.quantity
            item.save()
            order.ordered = True
            value = 0
##            for i in order.items.all():
##                value += Decimal(i.price) * Decimal(i.quantity)
            order.value = value
            order.save()

    elif order.type_order == "STOCK_OUT":
        for order_item in order.items.all():
            item = get_object_or_404(Product, slug=order_item.item.slug)
            item.quantity -= order_item.quantity
            item.save()            
            order.ordered = True
            value = 0
##            for i in order.items.all():
##                value += Decimal(i.item.price) * Decimal(i.quantity)
            order.value = value
            order.save()
            
    return redirect(order.get_absolute_url())


@login_required
def remove_from_cart(request, identifier):
    try:
        order = Order.objects.get(ordered=False)
    except:
        order = None

    item = get_object_or_404(OrderItem, identifier = identifier)
    order.items.remove(item)
    item.delete()
    messages.info(request, f"{item} a été supprimé de la commande.")
    if order.items.count() == 0:
        order.delete()
        return redirect("stock-manager:index")
    else:
        return redirect("stock-manager:order-summary")


class OrderList(ListView):
    queryset = Order.objects.filter(ordered = True)
    template_name = 'stock_manager/list/orders_list.html'
    paginate_by = 20


class OrderDetail(DetailView):
    template_name = 'stock_manager/detail/order_detail.html'
    model = Order
    # slug_field = 'slug'

    def get_object(self, **kwargs):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Order, slug=_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def email(request, object, content, email, email2, email3, email4, email5, email6):
    email = EmailMessage(object, content, to=[email, email2, email3, email4, email5, email6])
    email.send()
    return redirect(request.META.get('HTTP_REFERER'))


def stock_movement(request, slug):
    order = get_object_or_404(Order, slug=slug)
    template = loader.get_template('invoices/invoice.html')
    try:
        company = Company.objects.get(name='')
    except:
        company = ''
    context = {
        "user": request.user,
        "company": company,
        "order": order,
    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (order.ref_code)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def stock_status(request):
    product_list = Product.objects.all()
    try:
        company = Company.objects.get(name='')
    except:
        company = ''
    template = loader.get_template('invoices/stock_status.html')
    context = {
        "user": request.user,
        "company": company,
        "product_list": product_list,
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

class RecapPage(View):
    template_name = 'stock_manager/recap_page.html'

    def get(self, request):
        return render(request, "stock_manager/recap_page.html")


def recap(request):
    current_time = None
    if request.method == "GET":
        
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        start_date = parse_date(from_date)
        end_date = parse_date(to_date)
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = start_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        end_date = end_date.replace(hour = 23, minute = 59, second = 59, microsecond = 0)

        try:
            company = Company.objects.get(name ="")
        except:
            company = None
        orders_in = Order.objects.filter(type_order = "STOCK_ENTRY")
        orders_out = Order.objects.filter(type_order = "STOCK_OUT")
        orders_in = orders_in.filter(ordered_date__gte = start_date)
        orders_in = orders_in.filter(ordered_date__lte = end_date)
        orders_out = orders_out.filter(ordered_date__gte = start_date)
        orders_out = orders_out.filter(ordered_date__lte = end_date)

        products = Product.objects.all()

        for i in range(products.__len__()):
            products[i].calculated_bought_quantity = products[i].bought_quantity(start_date, end_date)
            products[i].calculated_sold_quantity = products[i].sold_quantity(start_date, end_date)
            products[i].calculated_cost = products[i].product_cost(start_date, end_date)
            products[i].calculated_benefit = products[i].benefit(start_date, end_date)

        cost = benefit = 0

        for i in orders_in:
            cost += i.get_amount()
        
        for i in orders_out:
            benefit += i.get_amount()

        
        template = loader.get_template('stock_manager/recap.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "company": company,
            "orders_in": orders_in,
            "orders_out": orders_out,
            "products": products,
            "cost": cost,
            "benefit": benefit,
        }
        html = template.render(context)
        pdf = render_to_pdf('stock_manager/recap.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "recap%s.pdf" % (timezone.now())
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")