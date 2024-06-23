from typing import List

from models import Base, Recipe, RecipeIngredient
from schemas import BaseRecipe
from sqlalchemy import desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import join, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()

DATA = {
    "recipes": {
        "name": ["макароны", "салат", "пицца"],
        "cooking_time_minutes": [10, 5, 2],
    },
    "recipe_ingredients": {
        "name": ["макароны", "салат", "пицца"],
        "cooking_time_minutes": [10, 5, 2],
        "list_of_ingredients": [
            "макароны, вода",
            "огурцы, помидоры",
            "пицца, микроволновка",
        ],
        "text_description": ["варёные макароны", "летний салат", "тёплая пицца"],
    },
}


async def completion_db() -> None:
    """Заполняет базу данных начальными данными из словаря DATA."""
    recipes = [
        Recipe(**{key: DATA["recipes"][key][i] for key in DATA["recipes"]})
        for i in range(len(DATA["recipes"]["name"]))
    ]

    ingredients = [
        RecipeIngredient(
            **{
                key: DATA["recipe_ingredients"][key][i]
                for key in DATA["recipe_ingredients"]
            }
        )
        for i in range(len(DATA["recipe_ingredients"]["name"]))
    ]

    session.add_all(recipes + ingredients)
    await session.commit()


async def init_db() -> None:
    """
    Инициализирует базу данных, создавая все таблицы и заполняя их начальными
        данными.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await completion_db()


async def get_all_recipes() -> List[RecipeIngredient]:
    """
    Возвращает список всех рецептов, отсортированных по количеству просмотров и
        времени приготовления.
    Returns:
        List[RecipeIngredient]: Список всех рецептов.
    """
    result = await session.execute(
        select(Recipe)
        .order_by(desc(Recipe.number_of_views))
        .order_by(Recipe.cooking_time_minutes)
    )
    return result.scalars().all()


async def get_recipe_by_id(recipe_id: int) -> RecipeIngredient:
    """
    Возвращает рецепт по его ID и увеличивает количество просмотров на 1.
    Args:
        recipe_id (int): ID рецепта.
    Returns:
        RecipeIngredient: рецепт.
    """
    query = (
        select(RecipeIngredient)
        .select_from(
            join(Recipe, RecipeIngredient, Recipe.name == RecipeIngredient.name)
        )
        .where(Recipe.recipe_id == recipe_id)
    )
    result = await session.execute(query)
    query = (
        update(Recipe)
        .where(Recipe.recipe_id == recipe_id)
        .values(number_of_views=Recipe.number_of_views + 1)
    )
    await session.execute(query)

    return result.scalars().one()


async def add_recipe(recipe: BaseRecipe, recipe_ingredients: BaseRecipe) -> None:
    """
    Добавляет новый рецепт и его ингредиенты в базу данных.
    Args:
        recipe (BaseRecipe): Новый рецепт.
        recipe_ingredients (BaseRecipe): Ингредиенты нового рецепта.
    """
    session.add(recipe)
    session.add(recipe_ingredients)
    await session.commit()
