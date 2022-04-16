from django.shortcuts import render
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from cartapp.models import Cart
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


class TitleContextMixin:

    def get_title(self):
        return getattr(self, 'title', '')

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        title = self.get_title()
        context.update(
            title=title
        )
        return context


class OrderListView(TitleContextMixin, ListView):
    model = Order
    title = 'Orders list'

    # template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(TitleContextMixin, CreateView):
    model = Order
    fields = []
    title = 'Create order'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            cart_items = Cart.objects.filter(user=self.request.user)
            if cart_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                                     extra=cart_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = cart_items[num].product
                    form.initial['quantity'] = cart_items[num].quantity
                    form.initial['price'] = cart_items[num].product.price
            else:
                formset = OrderFormSet()
        context.update(
            orderitems=formset
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            cart_items = Cart.objects.filter(user=self.request.user)
            cart_items.delete()

        if self.object.get_total_cost == 0:
            self.object.delete()

        return super(OrderCreateView, self).form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:orders_list')


class OrderUpdateView(TitleContextMixin,UpdateView):
    model = Order
    fields = []
    title = 'Update order'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)

        else:
            queryset = self.object.items.select_related()
            formset = OrderFormSet(instance=self.object, queryset = queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context.update(
            orderitems=formset
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost == 0:
            self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


def forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))
