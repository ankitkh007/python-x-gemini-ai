from core.gemini_client import client
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    name: str = Field(description="Name of the recipie.")
    ingredients: list[str] = Field(
        description="List of ingredients required for a particular recipe."
    )
    time_required: float = Field(
        description="otal time required to prepare the dish in hours."
    )


prompt = "List a few popular recipies for Chole Bhature."

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": {"type": "array", "items": Recipe.model_json_schema()},
    },
)

# print(Recipe.model_validate_json(response.text))
print(response.text)
