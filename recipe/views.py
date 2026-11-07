from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Recipe, Category, Comment, Rating, Favorite
from .forms import UserRegisterForm, CommentForm, RecipeForm, RecipeSearchForm
from django.core.paginator import Paginator
from django.db.models import Q

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    colors = ['bg-primary', 'bg-success', 'bg-danger', 'bg-warning text-dark', 'bg-info text-dark', 'bg-dark']

    cat_color_map = {}
    for i, cat in enumerate(categories):
        cat.color_class = colors[i % len(colors)]
        cat_color_map[cat.id] = cat.color_class

    form = RecipeSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        max_time = form.cleaned_data.get('max_cooking_time')

        if q:
            recipes = recipes.filter(
                Q(title__icontains=q) |
                Q(short_description__icontains=q) |
                Q(category__name__icontains=q)
            )
        if category:
            recipes = recipes.filter(category=category)
        if max_time:
            recipes = recipes.filter(cooking_time__lte=max_time)

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for recipe in page_obj:
        if recipe.category and recipe.category.id in cat_color_map:
            recipe.category.color_class = cat_color_map[recipe.category.id]

    context = {
        'recipes': page_obj,
        'categories': categories,
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'recipe_list.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all().order_by('-created_at')

    ratings = recipe.ratings.all()
    avg_rating = sum([r.score for r in ratings]) / len(ratings) if ratings else 0

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe

            rating_value = form.cleaned_data.get('rating')
            if rating_value:
                comment.rating = rating_value
                Rating.objects.update_or_create(
                    recipe=recipe,
                    user=request.user,
                    defaults={'score': rating_value}
                )

            comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = CommentForm()

    context = {
        'recipe': recipe,
        'comments': comments,
        'form': form,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, 'recipe_details.html', context)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    recipe_pk = comment.recipe.pk

    if comment.user == request.user or request.user.is_staff:
        comment.delete()

    return redirect('recipe_detail', pk=recipe_pk)

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user)
    comments = Comment.objects.filter(user=request.user)

    context = {
        'favorites': favorites,
        'comments': comments,
    }
    return render(request, 'profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
    return redirect('recipe_detail', pk=recipe.pk)