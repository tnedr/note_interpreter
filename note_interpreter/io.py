import csv
import yaml
from typing import List
from note_interpreter.models import Note, NoteBatch

class InputHandler:
    @staticmethod
    def read_notes_csv(path: str) -> List[Note]:
        notes = []
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip():
                    notes.append(Note(raw_input=row[0].strip()))
        return notes

    @staticmethod
    def read_user_memory_md(path: str) -> List[str]:
        memory = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('* '):
                    memory.append(line)
        return memory

    @staticmethod
    def read_classification_yaml(path: str) -> dict:
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_batch(notes_csv: str, memory_md: str, class_yaml: str) -> NoteBatch:
        notes = InputHandler.read_notes_csv(notes_csv)
        memory = InputHandler.read_user_memory_md(memory_md)
        config = InputHandler.read_classification_yaml(class_yaml)
        return NoteBatch(notes=notes, user_memory=memory, classification_config=config)

class OutputGenerator:
    @staticmethod
    def write_notes_csv(notes: List[Note], path: str):
        # For MVP1, just write raw_input and placeholder columns
        fieldnames = ['raw_input', 'interpreted_text', 'clarity_score', 'entity_type', 'intent']
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for note in notes:
                row = {
                    'raw_input': note.raw_input,
                    'interpreted_text': note.interpreted_text,
                    'clarity_score': note.clarity_score,
                    'entity_type': note.metadata.get('entity_type', ''),
                    'intent': note.metadata.get('intent', '')
                }
                writer.writerow(row) 