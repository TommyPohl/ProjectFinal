from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.utils.text import slugify
from ..models import Tag, Book
from ..forms import TagForm

@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag-list')
    else:
        form = TagForm()
    return render(request, 'books/create_tag.html', {'form': form})

def tag_list(request):
    tags = Tag.objects.all().order_by(Lower('name'))
    return render(request, 'books/tag_list.html', {'tags': tags})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    books = Book.objects.filter(tags=tag)
    return render(request, 'books/tag_detail.html', {
        'tag': tag,
        'books': books,
    })

@login_required
def edit_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            updated_tag = form.save(commit=False)
            updated_tag.slug = slugify(updated_tag.name)
            updated_tag.save()
            return redirect('tag-detail', slug=updated_tag.slug)
    else:
        form = TagForm(instance=tag)
    return render(request, 'books/edit_tag.html', {'form': form, 'tag': tag})


@login_required
def delete_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag-list')
    return render(request, 'books/delete_tag.html', {'tag': tag})


