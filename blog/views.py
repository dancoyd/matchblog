from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Category, Post


def home(request):
    latest_posts = Post.objects.filter(is_published=True)[:3]

    return render(request, "blog/home.html", {
        "latest_posts": latest_posts
    })


def about(request):
    return render(request, "blog/about.html")


def post_list(request):
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

    category_id = request.GET.get("category")

    if category_id:
        posts = posts.filter(category_id=category_id)

    return render(request, "blog/post_list.html", {
        "posts": posts,
        "categories": categories,
        "selected_category": category_id,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)

    return render(request, "blog/post_detail.html", {
        "post": post
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "La publicación fue creada correctamente.")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "blog/post_form.html", {
        "form": form,
        "title": "Crear publicación",
        "button_text": "Publicar",
    })


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "No tenés permiso para editar esta publicación.")
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "La publicación fue actualizada correctamente.")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {
        "form": form,
        "title": "Editar publicación",
        "button_text": "Guardar cambios",
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "No tenés permiso para eliminar esta publicación.")
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "La publicación fue eliminada correctamente.")
        return redirect("post_list")

    return render(request, "blog/post_confirm_delete.html", {
        "post": post
    })