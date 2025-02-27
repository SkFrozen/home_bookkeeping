from httpx import AsyncClient


class TestUserHandlers:

    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/users", json={"username": "username", "password": "password"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "created_at" in data

    async def test_get_token_pair_and_refresh_access_token(self, client: AsyncClient):
        # get token pair
        response = await client.post(
            "/users/token",
            json={
                "username": "username",
                "password": "password",
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        refresh_token = data["refresh_token"]
        # refresh access token
        response = await client.post(
            "users/token/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
