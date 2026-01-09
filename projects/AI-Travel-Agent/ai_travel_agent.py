from core.gemini_client import client
from google.genai import types
from pydantic import BaseModel, Field
import json


## Schema for structured output
class PlanSteps(BaseModel):
    step_name: str = Field(description="Step names for the goal will be stored here.")


class ExecuteSteps(BaseModel):
    task_name: str = Field(description="The name of current task/step.")
    action_performed: str = Field(
        description="Action performed for the particular task."
    )
    summary: str = Field(description="Summary of the entire process.")


def execute_step(step):
    prompt = (
        f"Execute this step: {step}. Describe what you did and summarize the result."
    )
    response = chat.send_message(
        prompt,
        config=types.GenerateContentConfig(
            response_json_schema={
                "type": "array",
                "items": ExecuteSteps.model_json_schema(),
            },
            response_mime_type="application/json",
            system_instruction="Answer within 30 words. Be specific to the point.",
        ),
    )
    result = json.loads(response.text)

    print("--------------------------------------")
    print("Ongoing Task : ", result[0]["task_name"])
    print("Action Performed: ", result[0]["action_performed"])
    print("Summary: ", result[0]["summary"])
    print("--------------------------------------")


def plan_steps():
    prompt = "Break the goal into clear, numbered steps."
    response = chat.send_message(
        prompt,
        config=types.GenerateContentConfig(
            response_json_schema={
                "type": "array",
                "items": PlanSteps.model_json_schema(),
            },
            response_mime_type="application/json",
            system_instruction="Answer within 20 words. Be specific to the point.",
        ),
    )
    plans = json.loads(response.text)

    steps = [plan["step_name"].strip() for plan in plans if plan["step_name"].strip()]

    return steps


def run_agent():
    ##steps planning
    steps = plan_steps()
    for step in steps:
        execute_step(step)
    print("\n All Steps Completed. Have a Safe Journey!!")


if __name__ == "__main__":
    print("Namaste, Welcome to Yatri-Mitra!!, Your AI Travel Agent.")
    print("Let's plan your journey........")
    source = input("Enter your Source: ")
    destination = input("Enter your Destination: ")
    print("---------------------------------------------------")

    goal = f"To Book a Railway ticket from {source} to {destination}."

    modified_prompt = f"""You're an expert virtual travel agent, having a very high experience of planning railway journeys in India.
    Your goal is {goal}. For know you just acknowledge the goal and going forward I'll ask you to create the plan and execute those plans."""

    chat = client.chats.create(model="gemini-2.5-flash-lite")

    chat.send_message(modified_prompt)

    ## run agent--> plan steps--> execute steps
    run_agent()
