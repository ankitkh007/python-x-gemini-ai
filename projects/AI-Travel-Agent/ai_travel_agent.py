from core.gemini_client import client
from google.genai import types
from pydantic import BaseModel, Field
from google.genai.errors import ClientError, ServerError
import json
import time

grounding_tool = types.Tool(google_search=types.GoogleSearch())


## Centralized prompt+config Wrapper for effiecient API error handling
def safe_send_message(chat, prompt, config, server_retries=2):
    try:
        return chat.send_message(prompt=prompt, config=config)

    except ClientError as e:
        if e.code == 429:
            print(
                "⚠️ API quota exhausted.💡Try changing the model or wait before retrying."
            )
            return None
        else:
            print("❌ Client error occurred.")
            return None

    except ServerError:
        if server_retries > 0:
            print("⚠️ Service temporarily unavailable (503). Retrying in 5 seconds...")
            time.sleep(5)  ## pauses for 5 seconds and then retries
            return safe_send_message(chat, prompt, config, server_retries - 1)
        else:
            print("❌ Service unavailable after retries. Skipping step.")
            return None

    except Exception:
        print("❌ Unexpected error occurred. Aborting...")
        return None


## Schema for structured output
class PlanSteps(BaseModel):
    step_name: str = Field(description="Step names for the goal will be stored here.")


class ExecuteSteps(BaseModel):
    task_name: str = Field(description="The name of current task/step.")
    action_performed: str = Field(
        description="Action performed for the particular task."
    )
    summary: str = Field(description="Summary of the entire process.")
    used_search: bool = Field(
        description="True if Google Search was used to complete this step, otherwise False."
    )


## Adding memory so that our agent gets the context of what it has already done
memory = [{"last_task": None, "summary": None, "used_search": None}]


## Phase 1(Execute Steps)
def reason_and_search(step, memory):
    prompt = f"""
            Last task done: {memory[-1]["last_task"]}, summary: {memory[-1]["summary"]}
        
            Now execute this step: {step}. Explain briefly what you did
            """
    config = (
        types.GenerateContentConfig(
            tools=[grounding_tool],
            system_instruction="""You are simulating actions.Do NOT ask user for inputs.Describe actions hypothetically.
                                Never wait for or request user input.If information is missing, assume reasonable defaults.
                                    - Do NOT output JSON 
                                    Use Google Search ONLY if: 
                                    - The task requires real-world or factual data 
                                    - The information is not available from prior steps. 
                                    If search is used, mention it clearly in the summary.""",
        ),
    )
    response = safe_send_message(chat, prompt=prompt, config=config)  ## calling Wrapper

    ## Error handling
    if response is None:
        return "Search failed. Proceed without external data."

    return response.text


## Phase 2(Execute Steps)
def structure_result(reasoning_text):
    prompt = f"""
                Based on the reasoning below, generate a JSON output
                matching this schema:
                
                - task_name
                - action_performed
                - summary
                - used_search (true/false)
                
                Reasoning:
                {reasoning_text}
                """
    config = (
        types.GenerateContentConfig(
            response_json_schema={
                "type": "array",
                "items": ExecuteSteps.model_json_schema(),
            },
            response_mime_type="application/json",
        ),
    )

    response = safe_send_message(chat, prompt=prompt, config=config)  ## calling Wrapper

    ## Error handling
    if response is None:
        raise RuntimeError("Structuring Failed!")
    return json.loads(response.text)


## Steps Execution in 2 phases
def execute_step(step, memory):
    # ---- PHASE 1 ----
    reasoning_text = reason_and_search(step, memory)

    # ---- PHASE 2 ----
    result = structure_result(reasoning_text)

    ## Filtering the required result for our memory
    required_memory = {
        "last_task": result[0]["task_name"],
        "summary": result[0]["summary"],
        "used_search": result[0]["used_search"],
    }

    ## Saving required memory after every successful execution
    memory.append(required_memory)

    ## Removes dummy dictionary after initial use
    dict_to_remove = {"last_task": None, "summary": None, "used_search": None}
    if dict_to_remove in memory:
        memory.remove(dict_to_remove)

    print("--------------------------------------")
    print("Ongoing Task : ", result[0]["task_name"])
    print("Action Performed: ", result[0]["action_performed"])
    print("Summary: ", result[0]["summary"])

    if result[0]["used_search"]:
        print("🔍 Google Search was used in this step")
    print("--------------------------------------")


## Steps Planning
def plan_steps():
    prompt = "Break the goal into clear, numbered steps."
    config = (
        types.GenerateContentConfig(
            response_json_schema={
                "type": "array",
                "items": PlanSteps.model_json_schema(),
            },
            response_mime_type="application/json",
            system_instruction="""Answer within 20 words. Be specific to the point.
                                You are planning steps for an AI agent that SIMULATES all actions internally.
                                Do NOT include steps that ask the user for input.
                                Assume all required information is already available.
                                Generate only executable, simulated steps.
                                """,
        ),
    )

    response = safe_send_message(chat, prompt=prompt, config=config)  ## Calling Wrapper

    ## Error handling
    if response is None:
        print("❌ Failed to generate plan. Please try again later.")
        return []  ## if steps planning failed return empty list

    plans = json.loads(response.text)

    steps = [plan["step_name"].strip() for plan in plans if plan["step_name"].strip()]

    return steps


def run_agent():
    ## steps planning
    steps = plan_steps()
    if not steps:
        print("❌ Planning failed. Agent cannot proceed. Sorry!")
        return

    for step in steps:
        execute_step(step, memory)  ## individual step execution
    print(
        "\n************************ All Steps Completed. Have a Safe Journey!! ************************"
    )
    print(
        "\n- - - - - - - - - - - - - - - - - - - - - - x-x-x - - - - - - - - - - - - - - - - - - - - - -"
    )


if __name__ == "__main__":
    print("Namaste, Welcome to Yatri-Mitra!!, Your AI Travel Agent.")
    print("Let's plan your journey........")
    source = input("Enter your Source: ")
    destination = input("Enter your Destination: ")
    print("--------------------------------------")

    goal = f"To Book a Railway ticket from {source} to {destination}."

    modified_prompt = f"""You're an expert virtual travel agent, having a very high experience of planning railway journeys in India.
    Your goal is {goal}. For know you just acknowledge the goal and going forward I'll ask you to create the plan and execute those plans."""

    chat = client.chats.create(model="gemini-2.5-flash")

    chat.send_message(modified_prompt)

    ## run agent--> plan steps--> execute steps(2-phases)
    run_agent()
