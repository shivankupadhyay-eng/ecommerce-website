from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from .forms import NewItemForm
from .models import Item,category

def items(request):
    query=request.GET.get('query','')
    categories=category.objects.all()
    items=Item.objects.filter(is_sold=False)
    
    if query:
        items=items.filter(Q(name__icontains=query)|Q(description__icontains=query))
    return render(request,"items/items.html",{
        'items':items,
        'query':query,
        'categories':categories,
    })

def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request,'items/details.html', {
        'item':item,
        'related_items':related_items
    })
    
@login_required
def new(request):
    if request.method == 'POST':
        form=NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=request.user
            item.save()
            return redirect('item:detail',pk=item.id)
    else:
        form=NewItemForm()
    
    return render(request,'items/form.html',{
    'form':form,
    'title':'New item'
        })
    
# @login_required
# def delete(request,pk):
#   item=get_object_or_404(Item,pk=pk,created_by=request.user)
#   item.delete()
  
#   return redirect('dashboard:index')

