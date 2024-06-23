""" Тестирование FastAPI приложения.
        старт тестов: pytest test_fastapi.py """

import pytest
from database import init_db
from httpx import ASGITransport, AsyncClient
from main import app

new_recipe_data = {
    "recipes": {"name": "суп", "cooking_time_minutes": 30},
    "recipe_ingredients": {
        "name": "суп",
        "cooking_time_minutes": 30,
        "list_of_ingredients": "пакетик супа, вода",
        "text_description": "невкусный суп",
    },
}


@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    """Инициализирует базу данных перед запуском тестов."""
    await init_db()


@pytest.mark.asyncio
async def test_get_all_recipes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_recipe_by_id():
    recipe_id = 1
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert "name" in json_response
    assert "cooking_time_minutes" in json_response
    assert "list_of_ingredients" in json_response
    assert "text_description" in json_response


@pytest.mark.asyncio
async def test_add_recipe():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/recipes", json=new_recipe_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response[0] == "Добавлен новый рецепт:"
    assert json_response[1]["name"] == new_recipe_data["recipes"]["name"]
    assert json_response[2]["name"] == new_recipe_data["recipe_ingredients"]["name"]
    assert (
        json_response[2]["list_of_ingredients"]
        == new_recipe_data["recipe_ingredients"]["list_of_ingredients"]
    )
    assert (
        json_response[2]["text_description"]
        == new_recipe_data["recipe_ingredients"]["text_description"]
    )
