from django.shortcuts import render
from blog.models import Post, Categoria

def blog(requests):
    posts = Post.objects.all()
    categorias = Categoria.objects.all()
    return render(
        requests, 
        "blog/blog.html",
        {
            "posts":posts,
            "categorias":categorias
        }
    )

def categoria(requests, id):
    categoria = Categoria.objects.get(id=id)
    posts = Post.objects.filter(categorias=categoria)
    return render(
        requests, 
        "blog/categorias.html",
        {
            "categoria":categoria,
            "posts":posts
        }
    )
