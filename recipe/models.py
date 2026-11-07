from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField("Название", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField("Фото рецепта", upload_to="recipes/", blank=True, null=True)
    short_description = models.CharField("Короткое описание", max_length=300, default="")
    ingredients = models.TextField("Ингредиенты")
    instructions = models.TextField("Инструкция по приготовлению")
    cooking_time = models.PositiveIntegerField("Время готовки (мин)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name="Рецепт")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField("Текст комментария")
    rating = models.PositiveIntegerField("Оценка (звёзды)", default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.recipe.title}"

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings', verbose_name="Рецепт")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    score = models.PositiveIntegerField("Оценка (от 1 до 5)")

    class Meta:
        unique_together = ('recipe', 'user')
    def __str__(self):
        return f"{self.user.username} оценил '{self.recipe.title}' на {self.score}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by', verbose_name="Рецепт")

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} добавил в избранное: {self.recipe.title}"