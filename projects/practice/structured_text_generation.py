from core.gemini_client import client
from pydantic import BaseModel, Field
import json
import pandas as pd


## class for structuring response as per requirement
class Recipe(BaseModel):
    name_of_dish: str = Field(description="Name of the recipie.")
    ingredients_required: list[str] = Field(
        description="List of ingredients required for a particular recipe."
    )
    time_required_in_hours: float = Field(
        description="otal time required to prepare the dish in hours."
    )


prompt = input("Enter your prompt for any dish recipe: ")

## structured response generation
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": {"type": "array", "items": Recipe.model_json_schema()},
    },
)

data = json.loads(response.text)  # loaded json response
df = pd.DataFrame(data)
df["ingredients_required"] = df["ingredients_required"].apply(lambda x: ",".join(x))
print(df)
df.to_excel("recipe.xlsx", sheet_name="Recipe", index=False)
print("✅ Recipe.xlsx saved!")
