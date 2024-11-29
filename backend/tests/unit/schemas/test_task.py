import pytest
from pydantic import ValidationError

from app.schemas.task import (
    TaskSchema,
    TaskUpdateSchema,
    Example,
    TestCase,
)


class TestTaskSchema:
    def test_valid_task_schema(self):
        data = {
            "name": "sum_with_inversion",
            "description": "Дано двузначное число. Нужно его развернуть, и сложить результат с исходным числом.",
            "input": "Целое число на отрезке 10..99.",
            "output": "Выражение вида: (исходное число) + (развернутое число) = (сумма).",
            "examples": [
                {"input": "82", "output": "82 + 28 = 110"},
                {"input": "27", "output": "27 + 72 = 99"},
            ],
            "test_cases": [
                {"input": "34", "expected_output": "34 + 43 = 77"},
                {"input": "45", "expected_output": "45 + 54 = 99"},
                {"input": "78", "expected_output": "78 + 87 = 165"},
                {"input": "12", "expected_output": "12 + 21 = 33"},
            ],
        }
        task = TaskSchema.model_validate(data)
        assert task.name == data["name"]
        assert len(task.examples) == 2
        assert len(task.test_cases) == 4
        assert isinstance(task.examples[0], Example)
        assert isinstance(task.test_cases[0], TestCase)

    def test_missing_required_fields(self):
        data = {
            "name": "sum_with_inversion",
            "description": "Дано двузначное число.",
        }
        with pytest.raises(ValidationError) as exc_info:
            TaskSchema.model_validate(data)
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any(error["loc"] == ("input",) for error in errors)
        assert any(error["loc"] == ("output",) for error in errors)

    def test_invalid_example_format(self):
        """Missing field output in examples"""
        data = {
            "name": "sum_with_inversion",
            "description": "Дано двузначное число.",
            "input": "Целое число на отрезке 10..99.",
            "output": "Выражение вида: (исходное число) + (развернутое число) = (сумма).",
            "examples": [{"input": "82"}],
            "test_cases": [
                {"input": "34", "expected_output": "34 + 43 = 77"},
            ],
        }
        with pytest.raises(ValidationError) as exc_info:
            TaskSchema.model_validate(data)
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("output" in error["loc"] for error in errors)

    def test_task_update_schema(self):
        update_data = {
            "name": "new_name",
            "examples": [{"input": "56", "output": "56 + 65 = 121"}],
        }
        update = TaskUpdateSchema.model_validate(update_data)
        assert update.name == "new_name"
        assert len(update.examples) == 1
        assert update.examples[0].input == "56"

    def test_empty_update_schema(self):
        update_data = {}
        update = TaskUpdateSchema.model_validate(update_data)
        assert update.name is None
        assert update.examples is None

    def test_invalid_test_case_format(self):
        data = {
            "name": "sum_with_inversion",
            "description": "Дано двузначное число.",
            "input": "Целое число на отрезке 10..99.",
            "output": "Выражение вида: (исходное число) + (развернутое число) = (сумма).",
            "examples": [
                {"input": "82", "output": "82 + 28 = 110"},
            ],
            "test_cases": [
                {"input": "34"},
            ],
        }
        with pytest.raises(ValidationError) as exc_info:
            TaskSchema.model_validate(data)
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("expected_output" in error["loc"] for error in errors)
