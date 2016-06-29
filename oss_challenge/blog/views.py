from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    form.fields['title'].widget.attrs['disabled'] = True
    return render(request, 'blog/post_edit.html', {'form': form})
