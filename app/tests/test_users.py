import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app

client = TestClient(app)

headers = {
    "Content-Type": "application/json",
}


@pytest.mark.anyio
async def test_users(client: AsyncClient):
    response = await client.get(
        url="/users",
        headers=headers
    )

    assert response.status_code == 200
