from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Menu, TableCart, CartItem, Order
from django import forms
from django.shortcuts import render
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def breakfast(request):
    breakfast_items = Menu.objects.filter(category='Breakfast', quantity=True)
    context = {'breakfast': breakfast_items}
    return render(request, 'breakfast.html', context)

def lunch(request):
    lunch_items = Menu.objects.filter(category='Lunch', quantity=True)
    context = {'lunch': lunch_items}
    return render(request, 'lunch.html', context)

def drinks(request):
    drinks_items = Menu.objects.filter(category='Drinks', quantity=True)
    context = {'drinks': drinks_items}
    return render(request, 'drinks.html', context)

def dessert(request):
    dessert_items = Menu.objects.filter(category='Dessert', quantity=True)
    context = {'dessert': dessert_items}
    return render(request, 'dessert.html', context)

def sides(request):
    sides_items = Menu.objects.filter(category='Sides', quantity=True)
    context = {'sides': sides_items}
    return render(request, 'sides.html', context)


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


def add_to_cart(request, item_id, table_number=1):
    item = get_object_or_404(Menu, pk=item_id)
    table_cart, created = TableCart.objects.get_or_create(table_number=table_number)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(item=item, quantity=quantity)
            table_cart.items.add(cart_item)
            return redirect('cart', table_number=table_number)
    else:
        form = AddToCartForm()

    context = {
        'item': item,
        'form': form
    }
    return render(request, 'add_to_cart.html', context)


def cart(request, table_number):
    table_cart = get_object_or_404(TableCart, table_number=table_number)
    items = table_cart.items.all()
    total_price = sum(item.item.price * item.quantity for item in items)

    context = {
        'table_number': table_number,
        'items': items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


def delete_item(request, table_number, item_id):
    table_cart = get_object_or_404(TableCart, table_number=table_number)
    item_to_delete = get_object_or_404(CartItem, pk=item_id)
    table_cart.items.remove(item_to_delete)
    return redirect('cart', table_number=table_number)


def make_order(request, table_number):
    table_cart = get_object_or_404(TableCart, table_number=table_number)
    items = table_cart.items.all()

    # Create order record in the database
    order = Order.objects.create(table_number=table_number)
    for item in items:
        order.items.add(item.item, through_defaults={'quantity': item.quantity})

    # Clear the cart for this table
    table_cart.items.clear()

    # Display confirmation message
    messages.success(request, 'Your order has been placed successfully!')

    # Persist the message across requests
    request.session['order_success_message'] = True

    return redirect('home')  # Redirect to home page after order submission