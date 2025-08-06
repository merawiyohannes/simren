from django.shortcuts import render, redirect, get_object_or_404
import os 

from .forms import AddItemForm, EditForm
from item.models import Item

def delete_view(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == "POST":
        item.delete()
        return redirect('home_view')
    return render(request, 'utility/delete.html', {"item": item})
      

def edit_view(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('detail_view', item.id)
        else:
            print(form.errors)
    else:
        form = EditForm(instance=item)
    return render(request, 'utility/edit.html', {"form":form})

def add_item_view(request):
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.created_by = request.user
            new.save()
            return redirect('home_view')
        else:
            print(form.errors)
        
    else:
        form = AddItemForm()   
    return render(request, "utility/add.html", {"form":form})
