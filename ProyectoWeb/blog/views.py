from django.shortcuts import render
from blog.models import Post, Categoria

def blog(requests):
    posts = Post.objects.all()
    return render(
        requests, 
        "blog/blog.html",
        {"posts":posts}
    )

def categoria(requests, id):
    categorias = Categoria.objects.get(id=id)
    posts = Post.objects.filter(categorias=categorias)
    return render(
        requests, 
        "blog/categorias.html",
        {
            "categorias":categorias,
            "posts":posts
        }
    )
