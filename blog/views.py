from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .forms import PostForm
from .models import Post

from django.views.generic import ListView, TemplateView


class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Hello, there!"
        return context



class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'

@login_required
def execute_post(request):
    """Handle create, edit, delete in one view"""
    action = request.POST.get('action')  # GET action from hidden form field
    post_id = request.POST.get('post_id')  # GET post ID if editing/deleting
    
    if request.method == 'GET':
        # Show form for create or edit
        post_id = request.GET.get('post_id')
        if post_id:
            # EDIT: Pre-fill form
            post = get_object_or_404(Post, pk=post_id, author=request.user)
            form = PostForm(instance=post)
            action = 'edit'
        else:
            # CREATE: Empty form
            form = PostForm()
            action = 'create'
        
        return render(request, 'blog/post_form.html', {
            'form': form, 
            'action': action,
            'post_id': post_id
        })
    
    elif request.method == 'POST':
        if action == 'delete':
            post = get_object_or_404(Post, pk=post_id, author=request.user)
            post.delete()
            return redirect('blog:post_list')
        
        elif action == 'edit':
            post = get_object_or_404(Post, pk=post_id, author=request.user)
            form = PostForm(request.POST, request.FILES, instance=post)
        
        else:  # action == 'create'
            form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            if action == 'create':
                post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
        
        return render(request, 'blog/post_form.html', {
            'form': form,
            'action': action,
            'post_id': post_id
        })

# CREATE - GET (show empty form) + POST (save)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user       # Add the current user as author
            post.save()                      # Now save
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()  # Empty form for GET request
    
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})

# EDIT - GET (show pre-filled form) + POST (update)
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)  # Only author can edit
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Pre-fill with existing data
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)  # Pre-fill form with post data
    
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'action': 'Edit'})

# DELETE - GET (confirmation) + POST (delete)
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})