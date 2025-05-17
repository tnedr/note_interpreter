import os
import tempfile
import yaml
from note_interpreter.io import InputHandler, OutputGenerator
from note_interpreter.models import Note, NoteBatch

def test_read_notes_csv():
    with tempfile.NamedTemporaryFile('w+', delete=False, newline='', encoding='utf-8') as f:
        f.write('note one\nnote two\n')
        f.flush()
        notes = InputHandler.read_notes_csv(f.name)
    assert len(notes) == 2
    assert notes[0].raw_input == 'note one'
    assert notes[1].raw_input == 'note two'
    os.remove(f.name)

def test_read_user_memory_md():
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as f:
        f.write('* memory one\n* memory two\n')
        f.flush()
        memory = InputHandler.read_user_memory_md(f.name)
    assert memory == ['* memory one', '* memory two']
    os.remove(f.name)

def test_read_classification_yaml():
    data = {'entity_types': ['task'], 'intents': ['@DO']}
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as f:
        yaml.dump(data, f)
        f.flush()
        config = InputHandler.read_classification_yaml(f.name)
    assert config['entity_types'] == ['task']
    assert config['intents'] == ['@DO']
    os.remove(f.name)

def test_write_notes_csv():
    notes = [Note(raw_input='n1', interpreted_text='i1', clarity_score=10, metadata={'entity_type': 'task', 'intent': '@DO'})]
    with tempfile.NamedTemporaryFile('w+', delete=False, newline='', encoding='utf-8') as f:
        OutputGenerator.write_notes_csv(notes, f.name)
        f.flush()
        f.seek(0)
        lines = f.readlines()
    assert 'raw_input' in lines[0]
    assert 'n1' in lines[1]
    os.remove(f.name)

def test_full_pipeline_integration():
    import tempfile
    import os
    import yaml
    from note_interpreter.io import InputHandler, OutputGenerator
    from note_interpreter.models import Note

    # Create sample input files
    with tempfile.NamedTemporaryFile('w+', delete=False, newline='', encoding='utf-8') as notes_f, \
         tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as mem_f, \
         tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as yaml_f, \
         tempfile.NamedTemporaryFile('w+', delete=False, newline='', encoding='utf-8') as out_f:
        notes_f.write('note one\nnote two\n')
        notes_f.flush()
        mem_f.write('* memory one\n* memory two\n')
        mem_f.flush()
        yaml.dump({'entity_types': ['task'], 'intents': ['@DO']}, yaml_f)
        yaml_f.flush()

        # Run pipeline
        batch = InputHandler.load_batch(notes_f.name, mem_f.name, yaml_f.name)
        # Add placeholder metadata for output
        for note in batch.notes:
            note.metadata = {'entity_type': 'task', 'intent': '@DO'}
        OutputGenerator.write_notes_csv(batch.notes, out_f.name)
        out_f.flush()
        out_f.seek(0)
        lines = out_f.readlines()

    # Check output
    assert 'raw_input' in lines[0]
    assert 'note one' in lines[1]
    assert 'task' in lines[1]
    assert 'note two' in lines[2]
    os.remove(notes_f.name)
    os.remove(mem_f.name)
    os.remove(yaml_f.name)
    os.remove(out_f.name) 