# note_interpreter

Ez a projekt egy Python alapú jegyzetértelmező rendszer.

## MVP 1: Running the Core Batch Note Interpreter

### Example Input Files
- `docs/examples/example_notes.csv`: Example notes (one per row)
- `docs/examples/example_user_memory.md`: Example user memory (Markdown bullets)
- `docs/examples/example_classification.yaml`: Example classification config (YAML)

### How to Run the Pipeline (MVP 1)
1. Ensure dependencies are installed (see `requirements.txt`).
2. Use the following code to load a batch and write output:

```python
from note_interpreter.io import InputHandler, OutputGenerator

batch = InputHandler.load_batch(
    'docs/examples/example_notes.csv',
    'docs/examples/example_user_memory.md',
    'docs/examples/example_classification.yaml'
)
OutputGenerator.write_notes_csv(batch.notes, 'output_notes.csv')
```

### How to Run the Tests

```bash
pytest tests
```

All tests should pass if the environment is set up correctly. 