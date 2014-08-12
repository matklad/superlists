from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item

def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    item = Item.objects.create(text=request.POST.get('item_text', ''))
    return redirect('/lists/the-only-list-in-the-world/')
