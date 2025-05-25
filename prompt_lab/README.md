# 🧪 Prompt Regression & Development Lab

## Overview

This project is a **modular, testable, and iterative framework** for developing and validating prompts used by LLM-based agents. It is designed as a *subproject* within a larger AI agent development ecosystem, and its goal is to ensure that prompts evolve in a controlled, regression-tested manner.

**This lab is designed for _stepwise, multi-turn prompt development_: you can build, test, and version agents that interact with the user in multiple rounds, asking clarifying questions if needed, not just static one-shot prompts.**

This lab provides the infrastructure to:
- Develop prompts in a structured and versioned way.
- Test prompts with realistic input scenarios.
- Execute lightweight agents with those prompts.
- Analyze and log the resulting outputs.
- Compare versions to detect regressions or improvements.

---

## Project Goals

- 🧠 Enable **prompt engineering as a software discipline**.
- 🔁 Facilitate **prompt versioning and regression detection**.
- ⚙️ Leverage **simple, reusable core libraries**: `PromptBuilder`, `AgentCore`, `Logger`.
- 📦 Isolate and test individual agent functionalities before full-scale integration.
- 💡 Serve as a test harness and ideation space for advanced agent behavior.
- 🧩 **Stepwise, multi-turn agent logic**: Support for agents that clarify, iterate, and refine their output through multiple prompt rounds.

---

## Project Structure

```plaintext
prompt-lab/
│
├── README.md ← This file
├── architecture.md ← System description & data flow
│
├── agents/ ← Agent definitions + prompt versions
│   └── clarifier/
│       ├── prompts/
│       ├── test_cases/
│       └── metadata.yaml
├── libs/ ← Reusable logic modules
│   ├── prompt_builder.py
│   ├── agent_core.py
│   └── logging_lib.py
├── test_inputs/ ← Shared input components (notes, memory, etc.)
├── results/ ← Test outputs, logs, and analysis results
├── scripts/ ← Main runners and orchestrators
│   ├── run_tests.py
│   ├── evaluate_outputs.py
│   └── main.py ← Optional CLI entrypoint
├── tests/ ← Unit tests for libs/
└── configs/ ← Optional: Promptfoo, LangSmith configs, env vars
```

See also: `docs/TESTING_MASTER_GUIDE.md`

---

## Core Workflow

1. 🛠 **Define stepwise agent behavior** – not just static prompts, but multi-turn, clarification-capable agents.
2. 🧱 **Build Prompt** – Use `PromptBuilder` to load and assemble prompt from YAML
3. 🧠 **Execute Agent** – Use `AgentCore` to run agent logic using the selected prompt
4. 📤 **Input & Output** – Feed test input (note, memory, etc.), including multi-step clarification scenarios
5. 🔬 **Evaluate Behavior** – Optionally define expected patterns or run diffing and scoring

**The workflow supports the development and testing of multi-step, clarification-capable agent pipelines.**

---

## Testing Architecture & Workflow

The prompt development and testing process consists of the following steps:

1. **Prompt versioning:**  
   Each agent's prompts are stored as separate YAML files, versioned in the `prompts/` folder.
2. **Test inputs:**  
   Realistic, diverse input YAMLs in the `test_inputs/` folder (e.g., notes, user memory, clarification history, multi-step examples).
3. **Automated test execution:**  
   The `run_prompt_tests.py` script runs every prompt version with every input and logs the results.  
   - The script uses PromptBuilder to generate the prompt.
   - The LLM (e.g., OpenAI GPT-4) is called with the generated prompt.
   - Outputs are logged and optionally compared to expected results.
4. **Promptfoo and LangSmith integration:**  
   These tools enable declarative, automated prompt testing and a web playground for rapid iteration.
5. **Results and regression:**  
   Tests are run for all prompt versions and inputs, so regressions are immediately visible.

---

## Reusable Core Libraries

| Module           | Description                                      |
|------------------|--------------------------------------------------|
| `prompt_builder` | Builds prompt strings from versioned YAML files |
| `agent_core`     | Minimal agent interface for executing prompts   |
| `logging_lib`    | Logs test results, diffs, and evaluations       |

---

## Example Test Case Structure

```yaml
agent: clarifier
prompt_version: v1
input:
  note: "User asked about magnesium absorption"
  memory: "Known deficiencies"
  # clarification_history: ["Does the user have gut issues?"]
expected:
  output_contains: ["magnesium", "absorption", "gut"]
```

---

## How To Run

1. Install dependencies:
   ```sh
   pip install -r requirements.txt  # or pipenv install -r prompt_testing/requirements.txt
   ```
2. Run the tests:
   ```sh
   python scripts/run_tests.py
   # or
   pipenv run promptfoo test promptfoo.yaml --provider openai:gpt-4
   ```
3. Start the web playground:
   ```sh
   pipenv run promptfoo web
   ```
4. LangSmith usage:
   - Register at https://smith.langchain.com/ and get your API key.
   - Set environment variables (e.g., `.env`):
     ```
     LANGCHAIN_API_KEY=your-key-here
     LANGCHAIN_TRACING_V2=true
     ```
   - Run the script:
     ```sh
     pipenv run python langsmith_test.py
     ```

---

## Roadmap

- Automated similarity and structure-based output evaluation
- Prompt diff visualizations
- LangSmith or Promptfoo integration (optional)
- CI-ready architecture for regression automation
- **Stepwise, multi-turn agent test harness and visualization**

---

## Philosophy

Don't build monolith prompts. Build evolving, testable, **stepwise**, intelligent components — just like great code.

---

## Meta Input/Output – The Prompt Lab as a System

**Meta Input (what you give to the Prompt Lab):**
- **Agent definition:**  
  What is the agent's goal?  
  What are its expected inputs/outputs?  
  What is the stepwise prompt pipeline (how many steps, what happens in each)?
- **Prompt versions:**  
  YAML files describing each prompt step.
- **Test cases:**  
  Input scenarios (possibly multi-step), expected outputs, clarification flows.
- **Evaluation criteria:**  
  What counts as a "good" output? (e.g., must contain certain info, must ask clarification if ambiguous, etc.)

**Meta Output (what the Prompt Lab produces):**
- **Test results:**  
  For each agent version and test case, what was the output? Did it match expectations?
- **Logs and diffs:**  
  Detailed logs, output differences between prompt versions.
- **Regression reports:**  
  Did a new prompt version break anything?
- **Prompt evolution history:**  
  How did the agent's stepwise logic change over time?

---

**Example:**

- Agent goal: "Interpret the user's note, ask for clarification if needed."
- Stepwise pipeline:  
  1. Step: note + memory → if ambiguous, ask clarification  
  2. Step: note + memory + clarification → final output
- Test case:  
  "Buy milk" + "User often forgets groceries" → "Do you need lactose-free milk?" → "Yes" → "User wants lactose-free milk."
- Expected behavior: always ask if ambiguous.
- Output: test results, logs, diffs, regressions, prompt pipeline evolution.

--- 