from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from .models import Item, List
from .forms import ItemForm, NewListForm, ExistingListForm
User = get_user_model()

def home_page(request):
    return render(request, 'home.dtl', {'form': ItemForm()})

def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.dtl', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    form = ExistingListForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.dtl', {'list': list_, 'form': form})

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.dtl', {
        'owner': owner
    })
