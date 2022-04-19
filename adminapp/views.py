from django.shortcuts import render
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from authapp.forms import ShopUserRegisterForm
from django.urls import reverse
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}: ')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


def user_check(user):
    if user.is_superuser:
        return True
    else:
        raise PermissionDenied


# Function Based Views - FBV for showing users
#
# @user_passes_test(user_check)
# def users(request,page=1):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     users_paginator = Paginator(users_list,2)
#     content = {
#         'title': title,
#         'objects': users_paginator.page(page)
#     }
#
#     return render(request, 'adminapp/users.html', content)
#


# CBV for showing users (FBV above on CBV)
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 4

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(user_check)
def user_create(request):
    title = "пользователи/создание"
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/update_user.html', content)


@user_passes_test(user_check)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/update_user.html', content)


@user_passes_test(user_check)
def user_update_age(request, pk, age):
    age = int(age)
    edit_user = get_object_or_404(ShopUser, pk=pk)
    edit_user.age = age
    edit_user.save()
    content = {'object': edit_user}
    result = render_to_string('adminapp/includes/inc_age.html', content)

    return JsonResponse({'result': result})


@user_passes_test(user_check)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# FBV to create category
# @user_passes_test(user_check)
# def category_create(request):
#     title = "категория/создание"
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#     return render(request, 'adminapp/update_category.html', content)

# CBV of FBV above
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


# FBV to update category
# @user_passes_test(user_check)
# def category_update(request, pk):
#     title = "категория/редактирование"
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {'title': title, 'update_form': category_form}
#     return render(request, 'adminapp/update_category.html', content)

# CBV of FBV above to update category
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price = F('price') * (1 - discount/100))
                db_profile_by_type(self.__class__,'UPDATE',connection.queries)
        return super().form_valid(form)

# FBV to delete a category
# @user_passes_test(user_check)
# def category_delete(request, pk):
#     title = 'категория/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'adminapp/category_delete.html', content)

# CBV of FBV above to delete a category
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    context_object_name = 'category_to_delete'

    # import pdb;pdb.set_trace()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(user_check)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('-is_active', 'name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


@user_passes_test(user_check)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title,
               'update_form': product_form,
               'category': category
               }

    return render(request, 'adminapp/product_update.html', content)


# FBV to detailed product
# @user_passes_test(user_check)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product, }
#
#     return render(request, 'adminapp/product_read.html', content)

# CBV of FBV above to detailed product
class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(user_check)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title,
               'update_form': edit_form,
               'category': edit_product.category
               }

    return render(request, 'adminapp/product_update.html', content)


#     product = get_object_or_404(Product, pk=pk)


@user_passes_test(user_check)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product}

    return render(request, 'adminapp/product_delete.html', content)
