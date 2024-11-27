from pydantic import BaseModel, RootModel


class Example(BaseModel):
    input: str
    output: str


class TestCase(BaseModel):
    input: str
    expected_output: str


class Task(BaseModel):
    description: str
    input: str
    output: str
    examples: list[Example]
    test_cases: list[TestCase]


class TasksSchema(RootModel[dict[str, Task]]):
    pass


if __name__ == "__main__":
    from pydantic import ValidationError

    data = {
        "sum_with_inversion": {
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
    }

    try:
        tasks = TasksSchema.model_validate(data)
        print(tasks.root["sum_with_inversion"].input)
    except ValidationError as e:
        print(e.json())
