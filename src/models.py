from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, relationship

Base = declarative_base()


class Recipe(Base):
    """
    Модель рецепта.
    Attributes:
        recipe_id (int): Уникальный идентификатор рецепта.
        name (str): Название рецепта, которое также является внешним ключом для
            таблицы 'recipe_ingredients'.
        cooking_time_minutes (int): Время приготовления в минутах.
        number_of_views (int): Количество просмотров рецепта.
        ingredients (relationship): Связь с моделью RecipeIngredient.
    """

    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        String, ForeignKey("recipe_ingredients.name"), nullable=False, unique=True
    )
    cooking_time_minutes = Column(Integer, comment="Время приготовления в минутах")
    number_of_views = Column(Integer, default=0)

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="recipe"
    )


class RecipeIngredient(Base):
    """
    Модель ингредиентов рецепта.
    Attributes:
        name (str): Название ингредиента, которое также является первичным ключом.
        cooking_time_minutes (int): Время приготовления в минутах.
        list_of_ingredients (str): Список ингредиентов.
        text_description (str): Текстовое описание рецепта.
        recipe (relationship): Связь с моделью Recipe.
    """

    __tablename__ = "recipe_ingredients"
    name = Column(String, primary_key=True, nullable=False, unique=True)
    cooking_time_minutes = Column(Integer, comment="Время приготовления в минутах")
    list_of_ingredients = Column(String, nullable=False)
    text_description = Column(String, nullable=False)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
