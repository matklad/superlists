from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from .models import Item, List
from .forms import ItemForm

def home_page(request):
    return render(request, 'home.dtl', {'form': ItemForm()})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

    return render(request, 'home.dtl', {'form': form})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    return render(request, 'list.dtl', {'list': list_, 'form': form})
