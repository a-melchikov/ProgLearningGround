from pydantic import BaseModel


class Example(BaseModel):
    input: str
    output: str


class TestCase(BaseModel):
    input: str
    expected_output: str


class TaskSchema(BaseModel):
    name: str
    description: str
    input: str
    output: str
    examples: list[Example]
    test_cases: list[TestCase]


class TaskCreateSchema(TaskSchema):
    pass


class TaskUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    input: str | None = None
    output: str | None = None
    examples: list[Example] | None = None
    test_cases: list[TestCase] | None = None


if __name__ == "__main__":
    from pydantic import ValidationError

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

    try:
        tasks = TaskSchema.model_validate(data)
        print(tasks)
    except ValidationError as e:
        print(e.json())
