from httpx import AsyncClient


class TestUserCrudException:

    async def test_exc_exist_username(self, client: AsyncClient, registered_user):
        response = await client.post(
            "/users/registration", json={"username": "test", "password": "password"}
        )
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert data.get("detail") == "Username already exists"
