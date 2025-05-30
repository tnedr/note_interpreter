## Runner/Bundle execution (2025-05-30)
- A runner a PromptBuilder-t használja a system prompt generálásához, a bundle inputját contextként adja át.
- A bundle initial_message mezőjét (ha van) user üzenetként küldi az agentnek.
- A logolás mindenhol a log.py log singletonnal történik.
- Az input context teljesen dinamikus, nincs beégetett mező vagy kulcs. 