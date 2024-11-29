import pytest
from pydantic import ValidationError

from app.schemas.code import Code


class TestCodeSchema:
    def test_valid_example(self):
        valid_code = {
            "code": 'number = int(input())\nreversed_number = int(str(number)[::-1])\nprint(f"{number} + {reversed_number} = {number + reversed_number}")'
        }
        code_instance = Code.model_validate(valid_code)
        assert code_instance.code == valid_code["code"]
        assert isinstance(code_instance, Code)

    def test_missing_code_field(self):
        with pytest.raises(ValidationError) as exc_info:
            Code()
        assert "Field required" in str(exc_info.value)

    def test_invalid_type(self):
        with pytest.raises(ValidationError) as exc_info:
            Code(code=123)
        assert "Input should be a valid string" in str(exc_info.value)

    def test_field_examples(self):
        example = Code.model_json_schema()["properties"]["code"]["examples"][0]
        code_instance = Code(code=example)
        assert code_instance.code == example
