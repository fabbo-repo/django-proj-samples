from django.shortcuts import render
from blog.models import Post

def blog(requests):
    posts = Post.objects.all()
    return render(
        requests, 
        "blog/blog.html",
        {"posts":posts}
    )