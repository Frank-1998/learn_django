from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from . forms import NewItemForm
# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_item = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_item
    })

@login_required # make sure the user is logged in, in order to add new items
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    form = NewItemForm()
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })
