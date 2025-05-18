# AI-Human Project Journal

- now 2025-05-17
- Started MVP 2 implementation: designed and implemented the pilot LLM agent (class, schema, test, and example usage) as the first step.
- Added a pilot micro-project (minimal LLM agent prototype) as a required first step in MVP 2 to validate structured LLM output before full integration.
- Added a detailed MVP 2 implementation plan (LLM batch processing, no clarification loop) to implementation_plan.md, including goal, checklist, AI suggestions, and progress tracking.
- Completed MVP 1 (core batch note interpreter): all tests pass, the pipeline works end-to-end, and documentation/examples are in place.
- Verified that all main documentation files (system overview, technical spec, functional spec, implementation plan) are consistent and aligned with the latest requirements (metadata fields, output format, batch agent, etc.).
- Decided to keep a running journal of project iterations and key decisions, with newest entries at the top, and to use a '- now [date]' marker for each day's records.
- Added detailed MVP milestones to the implementation plan for incremental delivery and validation.
- Established a clear, testable roadmap for the project with milestone-based MVPs.
- Restored and improved the technical specification, clarifying the batch-oriented LLM agent design and class structure.
- Renamed and reorganized documentation files for clarity and consistency.
- now 2025-05-18
- Refactored llm_agent.py to use more descriptive variable names for prompt injection, renamed template placeholders for clarity, and added a print statement to show the fully rendered prompt for debugging.
- Updated llm_agent.py to make the system prompt more explicit about always providing both 'entries' and 'new_memory_points' fields, and added a fallback in the tool function to handle missing fields gracefully.
- Clarified the required structure for 'entries' in the system prompt and tool docstring, and added validation to skip non-dict entries in the tool function in llm_agent.py.
- Implemented a clarification loop in llm_agent.py: the agent can ask clarification questions up to a maximum number of rounds, collects user answers, and finalizes with placeholders if the maximum is reached, following the functional specification.
- Updated the Classification YAML in the functional specification to include all entity_types and intents from the glossary for comprehensive metadata alignment.
- Set temperature=0.0 for all real LLM tests and the agent to ensure deterministic output, and updated both the agent and test code to support this.

