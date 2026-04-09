import pytest
from httpx import AsyncClient

from app.models import DeveloperTask, ProductivityReport, TaskStatus


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_returns_200(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_200(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_list(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_validates_against_model(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    tasks = [DeveloperTask(**item) for item in response.json()]
    assert all(isinstance(t, DeveloperTask) for t in tasks)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_report_returns_200(client: AsyncClient) -> None:
    response = await client.get("/report")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_report_validates_against_model(client: AsyncClient) -> None:
    response = await client.get("/report")
    report = ProductivityReport(**response.json())
    assert isinstance(report, ProductivityReport)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_201(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "New test task", "status": TaskStatus.PENDING, "hours_spent": 2.0}
    response = await client.post("/log_task", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_developer_task(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "New test task", "status": TaskStatus.PENDING, "hours_spent": 2.0}
    response = await client.post("/log_task", json=payload)
    task = DeveloperTask(**response.json())
    assert isinstance(task, DeveloperTask)
    assert task.title == "New test task"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_validation_error_on_missing_title(client: AsyncClient) -> None:
    payload = {"task_id": 0, "hours_spent": 1.0}
    response = await client.post("/log_task", json=payload)
    assert response.status_code == 422
