from httpx import AsyncClient


class TestUserCrudException:

    async def test_exc_exist_username(self, client: AsyncClient, registered_user):
        response = await client.post(
            "/users", json={"username": "test", "password": "password"}
        )
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data
        assert data.get("detail") == "User already exists"
