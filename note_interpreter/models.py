from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Note(BaseModel):
    """
    Represents a single user note and all associated data.
    """
    raw_input: str = Field(..., description="The original note text from the user.")
    scores: Dict[str, Any] = Field(default_factory=dict, description="Scoring fields (future use).")
    clarification_q_and_a: List[Dict[str, str]] = Field(default_factory=list, description="List of clarification Q&A pairs.")
    interpreted_text: str = Field('', description="The fully interpreted/enriched note (placeholder for MVP 1).")
    clarity_score: int = Field(0, description="Clarity score after enrichment (placeholder for MVP 1).")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata fields, e.g., entity_type and intent.")

class NoteBatch(BaseModel):
    """
    Represents a batch of notes, user memory, and classification config.
    """
    notes: List[Note] = Field(..., description="List of Note objects in the batch.")
    user_memory: List[str] = Field(default_factory=list, description="Narrative user memory entries.")
    classification_config: Dict[str, Any] = Field(default_factory=dict, description="Classification config loaded from YAML.")

class DataEntry(BaseModel):
    """
    Represents a single structured data entry returned by the LLM agent.
    Fields match the output schema: raw_text, interpreted_text, entity_type, intent, clarity_score.
    """
    raw_text: str = Field(..., description="The original note text from the user.")
    interpreted_text: str = Field(..., description="A full, self-contained, unambiguous sentence.")
    entity_type: str = Field(..., description="Entity type, e.g., task, project, idea, etc.")
    intent: str = Field(..., description="Intent, e.g., @DO, @PLAN, etc.")
    clarity_score: int = Field(..., description="Clarity score (0-100) of the interpreted output.")

class LLMOutput(BaseModel):
    """
    Represents the structured output from the LLM agent, including new memory points and tool call log.
    """
    entries: List[DataEntry]
    new_memory_points: List[str] = Field(default_factory=list, description="New bullet points to append to the Markdown memory.")
    tool_calls: List[dict] = Field(default_factory=list, description="List of tool calls made during the run.") 