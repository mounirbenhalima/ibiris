from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)
from Product.models import Brand, Product, Color, Flavor, Range

from Product.forms import (
    ColorForm,
    FlavorForm,
    ProductForm,
    BrandForm,
    RangeForm,
)


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



##--------------------------- Color Form --------------------------##

class ColorCreateView(CreateView):
    model = Color
    template_name = 'product/add_update/color_add.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Couleur'
        return context


class ColorUpdateView(UpdateView):
    template_name = 'product/add_update/color_add.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour une Couleur'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Color, slug=_slug)


class ColorListView(ListView):
    queryset = Color.objects.all()
    template_name = 'product/list/color_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ColorDeleteView(DeleteView):
    template_name = 'product/delete/color_delete.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Color, slug=_slug)
##------------------------- End color Form ------------------------##

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
        context["form_name"] = 'Ajouter un Nouveau Parfum'
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
        context["form_name"] = 'Mettre à jour un Parfum'
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