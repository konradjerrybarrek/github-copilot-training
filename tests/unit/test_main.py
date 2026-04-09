import pytest

from app.main import fetch_all_tasks, generate_productivity_report, MOCK_TASKS
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
