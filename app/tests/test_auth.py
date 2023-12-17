import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app

client = TestClient(app)

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer query_id=AAEWJzgGAAAAABYnOAZB_yAN&user=%7B%22id%22%3A104343318%2C%22first_name%22%3A%22grisha%200x%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22supervoid%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1702226671&hash=c58dce262d9c2df2495e8317ac41f4c0ce6af030a5c55cf3cabcdd50a4beda65"
}


@pytest.mark.anyio
async def test_auth(client: AsyncClient):
    response = await client.post(
        url="/auth",
        headers=headers
    )

    assert response.status_code == 200
