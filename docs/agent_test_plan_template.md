# Agent Test Plan Template

## 1. Purpose
Briefly describe the goal of the agent and what this test plan aims to verify.

## 2. Agent Description
- **Goal:** What is the agent supposed to do?
- **Inputs:** What are the expected input fields?
- **Outputs:** What is the expected output format/content?
- **Stepwise Logic:** How many steps/turns? When does clarification happen?

## 3. Test Cases

| Test Case | Input(s) | Expected Output | Notes |
|-----------|----------|----------------|-------|
| TC1       | ...      | ...            | ...   |
| TC2       | ...      | ...            | ...   |

*You can use YAML or table format for clarity.*

## 4. Evaluation Criteria
- What counts as a "pass"?
- How is correctness measured? (e.g., must contain certain keywords, must ask clarification if ambiguous, etc.)

## 5. Edge Cases
- List any edge cases or failure scenarios to test.

## 6. Regression/Versioning
- How will you track if a new prompt version breaks previous behavior?

## 7. Test Execution
- How will the tests be run? (e.g., automated script, manual review, etc.)
- Where will results be logged?

---

### Example Test Case (YAML)

```yaml
input:
  note: "Buy milk"
  memory: "User often forgets groceries"
expected:
  output_contains: ["milk", "groceries"]
  clarification_needed: true
clarification_input: "Lactose-free"
expected_final_output: "User wants to buy lactose-free milk."
``` 