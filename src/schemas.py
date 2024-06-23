from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    """
    Базовая схема для рецепта.
    Attributes:
        name (str): Название рецепта.
        cooking_time_minutes (int): Время приготовления в минутах.
        number_of_views (Optional[int]): Количество просмотров рецепта.
            По умолчанию None.
    """

    name: str
    cooking_time_minutes: int
    number_of_views: Optional[int] = None


class RecipeIn(BaseRecipe):
    """Схема для входных данных рецепта."""

    ...


class RecipeOut(BaseRecipe):
    """
    Схема для выходных данных рецепта.
    Attributes:
        recipe_id (int): Уникальный идентификатор рецепта.
    """

    recipe_id: int

    #  class Config:
    #      from_attributes = True

    model_config = ConfigDict(from_attributes=True)


class BaseRecipeIngredient(BaseModel):
    """
    Базовая схема для ингредиентов рецепта.
    Attributes:
        name (str): Название ингредиента.
        cooking_time_minutes (int): Время приготовления в минутах.
        list_of_ingredients (str): Список ингредиентов.
        text_description (str): Текстовое описание рецепта.
    """

    name: str
    cooking_time_minutes: int
    list_of_ingredients: str
    text_description: str


class RecipeIngredientIn(BaseRecipeIngredient):
    """Схема для входных данных ингредиентов рецепта."""

    ...


class RecipeIngredientOut(BaseRecipeIngredient):
    """Схема для выходных данных ингредиентов рецепта."""

    ...

    # class Config:
    #     from_attributes = True

    model_config = ConfigDict(from_attributes=True)


class CreateRecipeIn(BaseModel):
    """
    Схема для создания нового рецепта с ингредиентами.
    Attributes:
        recipes (RecipeIn): Данные рецепта.
        recipe_ingredients (RecipeIngredientIn): Данные ингредиентов рецепта.
    """

    recipes: RecipeIn
    recipe_ingredients: RecipeIngredientIn
