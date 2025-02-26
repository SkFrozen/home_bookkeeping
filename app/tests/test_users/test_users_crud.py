from httpx import AsyncClient


class TestUserCrud:

    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/users", json={"username": "username", "password": "password"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "created_at" in data
