from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Recipe, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email']


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, initial=5, widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте свой отзыв о рецепте...'
            }),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'image', 'short_description', 'ingredients', 'instructions', 'cooking_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Китайский салат'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Краткое описание в пару строк'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Каждый ингредиент с новой строки'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Пошаговый процесс приготовления'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'В минутах'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class RecipeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Поиск",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название блюда...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    max_cooking_time = forms.IntegerField(
        required=False,
        label="Макс. время готовки (мин)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: 45'
        })
    )