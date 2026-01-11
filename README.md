# Python × Gemini AI – Agent-Based Automation Framework

## 🚀 Overview
This repository demonstrates how to build **robust AI agents using Python and Google's Gemini API**.
The project focuses on **agent-style planning, execution, memory handling, structured outputs, and API-failure resilience**.

As a practical use case, the framework implements an **AI Travel Agent** that plans and executes railway journey tasks step-by-step.

---

## ✨ Key Highlights
- 🧠 Agent-based task planning and execution
- 🔁 Two-phase execution (Reasoning → Structured Output)
- 📦 Structured JSON responses using Pydantic schemas
- 🔍 Optional Google Search tool grounding
- 🧾 Memory-based context tracking across steps
- ⚠️ Robust API error handling (quota exhaustion, retries, graceful fallback)

---

## 🏗️ Project Architecture

```text
python-x-gemini-ai/
│
├── core/
│   ├── config.py              # Environment & configuration management
│   └── gemini_client.py       # Gemini API client initialization
│
├── projects/
│   └── AI-Travel-Agent/
│   |    └── ai_travel_agent.py # Main AI agent logic (planning + execution)
|   |
|   ├──practice/                  # Experimental / practice scripts
│   |
|   └──images/                    # Screenshots of agent execution
│
├── README.md
├── .env
└── .gitignore


## 📷 Sample Execution

### Successful Execution
![Agent Success](projects\images\agent_success.png)

### Graceful Failure Handling
![API Failure](projects\images\api_failure_handling.png)
