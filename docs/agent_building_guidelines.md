# 🧩 System Overview

## Objective

Develop an interactive AI system using LangChain that:

- Engages in multi-turn conversations with users
- Utilizes a Markdown document as the agent's long-term memory
- Incorporates a partially filled CSV template into the prompt
- Collects and validates structured data inputs from the user
- Generates a complete CSV file with predefined fields
- Updates the Markdown memory by appending new bullet points

# 🛠️ Implementation Steps

## 1. Define the Output Schema

Use Pydantic to define the expected structure of the data collected from the user.

```python
from pydantic import BaseModel, Field
from typing import List

class DataEntry(BaseModel):
    field1: str = Field(description="Description for field1")
    field2: int = Field(description="Description for field2")
    # Add more fields as needed

class LLMOutput(BaseModel):
    entries: List[DataEntry]
    new_memory_points: List[str] = Field(description="New bullet points to append to the Markdown memory")
```

## 2. Configure the LLM with Structured Output

Leverage LangChain's `with_structured_output()` to ensure the LLM's responses conform to the defined schema.

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", openai_api_key="your-api-key")
structured_llm = llm.with_structured_output(LLMOutput)
```

## 3. Prepare the Prompt with Existing Data

Integrate the existing Markdown memory and the partially filled CSV into the prompt to provide context to the LLM.

```python
prompt = f"""
You are an AI agent assisting with data entry.

Current Memory:
{markdown_memory}

Current CSV Data:
{csv_data}

Please interact with the user to collect the necessary information to complete the CSV and update the memory.
"""
```

## 4. Engage in Interactive Session

Implement a loop that continues to collect `DataEntry` instances until the user indicates completion.

```python
while not session_complete:
    user_input = input("Please provide the next data entry or type 'done' to finish: ")
    if user_input.lower() == 'done':
        session_complete = True
    else:
        # Process the user input and collect data
        pass
```

## 5. Invoke the LLM and Obtain Structured Data

Upon user completion, prompt the LLM to generate the structured output.

```python
response = structured_llm.invoke(prompt)
```

## 6. Generate the CSV File

Transform the entries from the LLM's response into a CSV file.

```python
import csv

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Field1', 'Field2'])  # Add headers as per your schema
    for entry in response.entries:
        writer.writerow([entry.field1, entry.field2])
```

## 7. Update the Markdown Memory

Append the new bullet points to the existing Markdown memory.

```python
with open('memory.md', mode='a') as file:
    for point in response.new_memory_points:
        file.write(f"* {point}\n")
```

# ✅ Recommendation

By integrating the existing Markdown memory and partially filled CSV into the prompt, the LLM gains the necessary context to intelligently complete the CSV and update the memory. Utilizing Pydantic schemas ensures that the output adheres to a predefined structure, facilitating reliable post-processing.

This approach provides a robust framework for interactive data collection and memory management, aligning with your project's objectives.
