from pydantic import BaseModel, Field


class Code(BaseModel):
    code: str = Field(
        ...,
        title="User Code",
        description="The code to be executed.",
        examples=[
            'number = int(input())\nreversed_number = int(str(number)[::-1])\nprint(f"{number} + {reversed_number} = {number + reversed_number}")',
        ],
    )
