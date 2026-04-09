import pytest

from app.main import fetch_all_tasks, generate_productivity_report, get_task_status, log_task, MOCK_TASKS
from app.models import DeveloperTask, ProductivityReport, TaskStatus


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list() -> None:
    result = await fetch_all_tasks()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_developer_task_instances() -> None:
    result = await fetch_all_tasks()
    assert all(isinstance(task, DeveloperTask) for task in result)


@pytest.mark.asyncio
async def test_fetch_all_tasks_matches_mock_db() -> None:
    result = await fetch_all_tasks()
    assert len(result) == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_generate_productivity_report_returns_model() -> None:
    result = await generate_productivity_report()
    assert isinstance(result, ProductivityReport)


@pytest.mark.asyncio
async def test_generate_productivity_report_total_tasks() -> None:
    result = await generate_productivity_report()
    assert result.total_tasks == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_generate_productivity_report_completion_rate_bounds() -> None:
    result = await generate_productivity_report()
    assert 0.0 <= result.completion_rate <= 1.0


@pytest.mark.asyncio
async def test_generate_productivity_report_completed_tasks_counts_complete_status() -> None:
    result = await generate_productivity_report()
    expected = sum(1 for t in MOCK_TASKS.values() if t.status == TaskStatus.COMPLETE)
    assert result.completed_tasks == expected


@pytest.mark.asyncio
async def test_generate_productivity_report_total_hours() -> None:
    result = await generate_productivity_report()
    expected = round(sum(t.hours_spent for t in MOCK_TASKS.values()), 2)
    assert result.total_hours_spent == expected


@pytest.mark.asyncio
async def test_get_task_status_returns_status_for_existing_task() -> None:
    result = await get_task_status(1)
    assert result == {"task_id": 1, "status": TaskStatus.COMPLETE}


@pytest.mark.asyncio
async def test_get_task_status_returns_error_for_missing_task() -> None:
    result = await get_task_status(9999)
    assert result == {"error": "Task not found"}


@pytest.mark.asyncio
async def test_log_task_assigns_new_id() -> None:
    initial_max = max(MOCK_TASKS.keys())
    new_task = DeveloperTask(task_id=0, title="Test task", status=TaskStatus.PENDING, hours_spent=1.0)
    result = await log_task(new_task)
    assert result.task_id == initial_max + 1


@pytest.mark.asyncio
async def test_log_task_stores_task_in_mock_db() -> None:
    new_task = DeveloperTask(task_id=0, title="Stored task", status=TaskStatus.IN_PROGRESS, hours_spent=3.0)
    result = await log_task(new_task)
    assert result.task_id in MOCK_TASKS
    assert MOCK_TASKS[result.task_id].title == "Stored task"


@pytest.mark.asyncio
async def test_log_task_returns_developer_task_instance() -> None:
    new_task = DeveloperTask(task_id=0, title="Return type task", status=TaskStatus.PENDING, hours_spent=0.5)
    result = await log_task(new_task)
    assert isinstance(result, DeveloperTask)
