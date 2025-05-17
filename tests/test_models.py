from note_interpreter.models import Note, NoteBatch
import pytest


def test_note_creation():
    note = Note(raw_input="Test note")
    assert note.raw_input == "Test note"
    assert note.scores == {}
    assert note.clarification_q_and_a == []
    assert note.interpreted_text == ''
    assert note.clarity_score == 0
    assert note.metadata == {}


def test_note_batch_creation():
    notes = [Note(raw_input="Note 1"), Note(raw_input="Note 2")]
    batch = NoteBatch(notes=notes, user_memory=["* User context"], classification_config={"entity_types": ["task"]})
    assert len(batch.notes) == 2
    assert batch.user_memory == ["* User context"]
    assert batch.classification_config["entity_types"] == ["task"]


def test_note_validation():
    with pytest.raises(Exception):
        Note()  # raw_input is required


def test_note_serialization():
    note = Note(raw_input="Serialize me", metadata={"entity_type": "task", "intent": "@DO"})
    data = note.dict()
    note2 = Note(**data)
    assert note2.raw_input == "Serialize me"
    assert note2.metadata["entity_type"] == "task"
    assert note2.metadata["intent"] == "@DO" 