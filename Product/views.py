from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import loader, Context

from xhtml2pdf import pisa
from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)
from Product.models import Brand, Product, Batch, Flavor, Range
from Company.models import Company

from Product.forms import (
    FlavorForm,
    ProductForm,
    BrandForm,
    RangeForm,
)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)

    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class ProductIndexView(TemplateView):
    template_name = 'product/index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductDeleteView(DeleteView):
    template_name = 'product/delete/product_delete.html'
    success_url = reverse_lazy('product:index')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=_slug)

# ##------------------------- Brand Views -------------------------##


class BrandCreateView(CreateView):
    model = Brand
    template_name = 'product/add_update/brand_add.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Marque'
        return context


class BrandUpdateView(UpdateView):
    template_name = 'product/add_update/brand_add.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour une Marque'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Brand, slug=_slug)


class BrandListView(ListView):
    queryset = Brand.objects.all()
    template_name = 'product/list/brand_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BrandDeleteView(DeleteView):
    template_name = 'product/delete/brand_delete.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Brand, slug=_slug)

# ##----------------------- End Brand Form -----------------------##

# ##------------------------- Range Views -------------------------##


class RangeCreateView(CreateView):
    model = Range
    template_name = 'product/add_update/range_add.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Gamme'
        return context


class RangeUpdateView(UpdateView):
    template_name = 'product/add_update/range_add.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour Une Gamme'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Range, slug=_slug)


class RangeListView(ListView):
    queryset = Range.objects.all()
    template_name = 'product/list/range_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RangeDeleteView(DeleteView):
    template_name = 'product/delete/range_delete.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Range, slug=_slug)

# ##----------------------- End Range Form -----------------------##

##--------------------------- Flavor Form --------------------------##


class FlavorCreateView(CreateView):
    model = Flavor
    template_name = 'product/add_update/flavor_add.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouvel Arôme'
        return context


class FlavorUpdateView(UpdateView):
    template_name = 'product/add_update/flavor_add.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Arôme'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Flavor, slug=_slug)


class FlavorListView(ListView):
    queryset = Flavor.objects.all()
    template_name = 'product/list/flavor_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FlavorDeleteView(DeleteView):
    template_name = 'product/delete/flavor_delete.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Flavor, slug=_slug)
##------------------------- End Flavor Form ------------------------##

##------------------------- Product Form ------------------------##
class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/add_update/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('product:products')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter Un Nouveau Produit'
        return context


class ProductUpdateView(UpdateView):
    template_name = 'product/add_update/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('product:products')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour Un Produit'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=_slug)



class ProductListView(ListView):
    template_name = 'product/list/product_list.html'
    # paginate_by = 10
    queryset = Product.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
##------------------------- End Product Form ------------------------##

def batch_list(request):
    batches = Batch.objects.exclude(quantity = 0).all()
    products = Product.objects.exclude(quantity = 0).all()
    return render(request, 'product/list/batch_list.html', context={'batches': batches, 'products': products})

def print_batch_code(request, slug):
    batch = get_object_or_404(Batch, slug=slug)
    template = loader.get_template('product/batch_ticket.html')
    try:
        company = Company.objects.get(name='')
    except:
        company = ''
    context = {
        "company": company,
        "batch": batch,

    }
    html = template.render(context)
    pdf = render_to_pdf('product/batch_ticket.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" % (batch.ref)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")