""" старт сервера:  uvicorn main:app --reload """

from typing import List, Tuple

from fastapi import FastAPI

import models
import schemas
from database import (
    add_recipe,
    engine,
    get_all_recipes,
    get_recipe_by_id,
    init_db,
    session,
)

app = FastAPI()
ааааааааааааааааааааааааааааааааааааааааааа

@app.on_event("startup")
async def shutup() -> None:
    """Событие запуска приложения. Инициализирует базу данных."""
    await init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Событие завершения работы приложения. Закрывает сессию и освобождает
        ресурсы движка.
    """
    await session.close()
    await engine.dispose()


@app.get("/recipes/", response_model=List[schemas.RecipeOut])
async def get_all_recipes_endpoint() -> List[models.Recipe]:
    """
    Эндпоинт для получения списка всех рецептов.
        Returns:
            List[models.Recipe]: Список всех рецептов.
    """
    return await get_all_recipes()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeIngredientOut)
async def get_recipe_by_id_endpoint(recipe_id: int) -> models.RecipeIngredient:
    """
    Эндпоинт для получения рецепта по его ID.
    Args:
        recipe_id (int): ID рецепта.
    Returns:
        models.RecipeIngredient: Найденный рецепт.
    """
    return await get_recipe_by_id(recipe_id)


@app.post("/recipes")
async def add_recipe_endpoint(
    new_recipe: schemas.CreateRecipeIn,
) -> Tuple[str, schemas.RecipeOut, schemas.RecipeIngredientOut]:
    """
    Эндпоинт для добавления нового рецепта.
    Args:
        new_recipe (schemas.CreateRecipeIn): Данные нового рецепта.
    Returns:
        Tuple[str, schemas.RecipeOut, schemas.RecipeIngredientOut]: Сообщение о
         добавлении, данные добавленного рецепта и его ингредиентов.
    """
    recipe_data = new_recipe.recipes.model_dump()
    recipe = models.Recipe(**recipe_data)
    ingredients_data = new_recipe.recipe_ingredients.model_dump()
    recipe_ingredients = models.RecipeIngredient(**ingredients_data)
    await add_recipe(recipe, recipe_ingredients)
    recipe_out = schemas.RecipeOut.model_validate(recipe, from_attributes=True)
    ingredients_out = schemas.RecipeIngredientOut.model_validate(
        recipe_ingredients, from_attributes=True
    )

    return "Добавлен новый рецепт:", recipe_out, ingredients_out
